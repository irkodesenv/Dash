  $(document).ready(function() {
    
        var data_formatada = data_atual();
        $("#data_vencimento").text(data_formatada);
        $("#btn_limpa_filtro").css("display", "None");
        
        pegar_data_filtro(data_formatada,data_formatada)
        var range_datas = $("#flatpickr-range").val();
        var datas_formatadas = formata_range_datas(range_datas);
        
        retorna_dados_dash(datas_formatadas.data_inicial, datas_formatadas.data_final);
        recuperar_doctos_indefinidos(datas_formatadas.data_inicial, datas_formatadas.data_final);
        //carrega_dados_ranking_doctos_indefinidos();

        setInterval(function() {        
          var range_datas = $("#flatpickr-range").val();
          var datas_formatadas = formata_range_datas(range_datas);
          retorna_dados_dash(datas_formatadas.data_inicial, datas_formatadas.data_final);
          recuperar_doctos_indefinidos(datas_formatadas.data_inicial, datas_formatadas.data_final);
        }, 60000);


  })


//função para retornar dados dashboard
function retorna_dados_dash(datini,datfim){
  $('#msg_erro').text("")
  $('#msg_erro').css('display','none')

  $.ajax({
    url: carrega_dados_dash,
    type: 'POST',
    dataType: 'JSON',
    data: { "datini":datini,"datfim":datfim,"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val() },
    success: function (data) {
      print_dados_na_tela(data.data);
  
      carrega_ranking(data.data);
      carrega_ranking2(data.data);
      

    },
    error: function (error) {
        console.error('Erro na requisição:', error);
        $('#msg_erro').text("Estamos com instabilidade na conexão de clientes, por favor acionar a equipe responsável.")
        $('#msg_erro').css('display','block')
    }
});

}  

//função para retornar dados de doctos indefinidos
function recuperar_doctos_indefinidos(datini,datfim){
  $('#msg_erro').text("")
  $('#msg_erro').css('display','none')

  $.ajax({
    url: carrega_dados_doctos_indefinidos,
    type: 'POST',
    dataType: 'JSON',
    data: { "datini":datini,"datfim":datfim,"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val() },
    success: function (data) {
      carrega_lista_doctos_indefinidos(data.data.ListaIndefinidos);

    },
    error: function (error) {
        console.error('Erro na requisição:', error);
        $('#msg_erro').text("Estamos com instabilidade na conexão de clientes, por favor acionar a equipe responsável.")
        $('#msg_erro').css('display','block')
    }
});

}


//função para escrever dados na tela
function print_dados_na_tela(data) {
  $('#total_clientes').text(data.Totais.TotalEmpresas);
  $('#qtd_doc').text(data.Totais.TotalQuantidadeDocumentos);
  
  $('#qtd_nexxera').text(data.Totais.TotalNexxera);
  $('#qtd_cnab').text(data.Totais.TotalRemessas);
  $('#qtd_manual').text(data.Totais.TotalManual);
  
  var totalValor = data.Totais.TotalValor;
  var valorFormatado = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(totalValor);

  $('#val_pag').text(valorFormatado);

}


//Função que monta o rankin 1 ao 8
function carrega_ranking(data) {
  
  const tbody = $('#ranking_body');
  tbody.empty();
  const top6 = data.ListaEmpresas.slice(0, 8);
  console.log(data)
  top6.forEach((item, index) => {

    const valorItem = parseMonetaryValue(item.valortotal);
    const percentual = ((valorItem / data.Totais.TotalValor) * 100).toFixed(2);
    
    const logoPath = `/templates/static/media/logos_emp/${item.codigoempresa}.png`;
    const defaultLogo = '/templates/static/media/logos_emp/default.png';
    
    if(item.doctosfaltantes==0){
      var doctosClass ="heading"
    }
    else{
      var doctosClass ="danger"
    }
    
    const row = `
      <tr>
        <td>${index + 1}</td>
        <td class="padding-left-0">
          <div class="d-flex align-items-center">
            <a href="#" 
              class="d-flex align-items-center text-decoration-none"
              data-bs-toggle="modal" 
              data-bs-target="#modalDocumentos"
              onclick="recupera_dados_doctos_gerais(${item.codigoempresa})">
              <img src="${logoPath}" onerror="this.onerror=null;this.src='${defaultLogo}';" height="24" width="24" class="me-3" />
              <span class="text-heading">${item.razao}</span>
            </a>
          </div>
        </td>
        <td class="text-${doctosClass}">
          <a href="#" 
            class="d-flex align-items-center text-decoration-none text-${doctosClass}"
            data-bs-toggle="modal" 
            data-bs-target="#modalDocumentos"
            onclick="recupera_dados_doctos_gerais(${item.codigoempresa})">
            ${item.quantidadedocumentos}/${item.doctosfaltantes}
        </a>
      </td>
        <td class="text-heading">R$ ${(item.valortotal)}</td>
        <td>
          <div class="d-flex justify-content-between align-items-center gap-4">
            <div class="progress w-100" style="height: 10px">
              <div class="progress-bar bg-info" role="progressbar" style="width: ${percentual}%"
                aria-valuenow="${percentual}" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <small class="fw-medium">${percentual}%</small>
          </div>
        </td>
      </tr>
    `;

    tbody.append(row);
  });
}


//Função que monta o rankin 9 ao 16
function carrega_ranking2(data) {
  
  const tbody = $('#ranking_body2');
  tbody.empty();
  const top6 = data.ListaEmpresas.slice(8, 16);

  top6.forEach((item, index) => {
    
    const valorItem = parseMonetaryValue(item.valortotal);
    const percentual = ((valorItem / data.Totais.TotalValor) * 100).toFixed(2);
    //const percentual = ((item.quantidadedocumentos / (data.Totais.TotalQuantidadeDocumentos)) * 100).toFixed(2);

    const logoPath = `/templates/static/media/logos_emp/${item.codigoempresa}.png`;
    const defaultLogo = '/templates/static/media/logos_emp/default.png';
    //<img src="/templates/static/media/logos_emp/${item.codigoempresa}.png" height="24" width="24" class="me-3" />

    if(item.doctosfaltantes==0){
      var doctosClass ="heading"
    }
    else{
      var doctosClass ="danger"
    }
    
    const row = `
      <tr>
        <td>${index + 9}</td>
        <td class="padding-left-0">
          <div class="d-flex align-items-center">
            <a href="#" 
              class="d-flex align-items-center text-decoration-none"
              data-bs-toggle="modal" 
              data-bs-target="#modalDocumentos"
              onclick="recupera_dados_doctos_gerais(${item.codigoempresa})">
              <img src="${logoPath}" onerror="this.onerror=null;this.src='${defaultLogo}';" height="24" width="24" class="me-3" />
              <span class="text-heading">${item.razao}</span>
            </a>
          </div>
        </td>
        <td class="text-${doctosClass}">
          <a href="#" 
            class="d-flex align-items-center text-decoration-none text-${doctosClass}"
            data-bs-toggle="modal" 
            data-bs-target="#modalDocumentos"
            onclick="recupera_dados_doctos_gerais(${item.codigoempresa})">
            ${item.quantidadedocumentos}/${item.doctosfaltantes}
        </a>
      </td>
        <td class="text-heading">R$ ${(item.valortotal)}</td>
        <td>
          <div class="d-flex justify-content-between align-items-center gap-4">
            <div class="progress w-100" style="height: 10px">
              <div class="progress-bar bg-info" role="progressbar" style="width: ${percentual}%"
                aria-valuenow="${percentual}" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <small class="fw-medium">${percentual}%</small>
          </div>
        </td>
      </tr>
    `;

    tbody.append(row);
  });

}


//Função que monta o modal de doctos indefinidos
function carrega_lista_doctos_indefinidos(data) {
  const tbody = $('#ranking_lista');
  tbody.empty();
  
  

  data.forEach((item, index) => {


    valor_formatado = formatarMoeda(parseFloat(item.Valor.toString().replace(".","").replace(",","")) /100)
   
    const row = `
      <tr>
              <td>
                <div class="d-flex align-items-center">
                  <span class="text-heading">${item.CodCli} - ${item.DescricaoEmpresa.substring(0,25)}</span>
                </div>
              </td>
              <!-- Dados de Demonstração de Documentos Indefinidos -->
              <td class="text-danger f-bold">${item.DataVencimento}</td>
              <td class="text-heading">${item.DescricaoFornecedor.substring(0,25)}</td>
              <td class="text-heading">${item.NumeroDocumento}</td>
              <td class="text-heading">${valor_formatado}</td>
              </td>        
            </tr>
    `;

    tbody.append(row);
  });

}


function formatarMoeda(valor) {
  return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}


function data_atual(){
    
  var data_atual = new Date();
  var data_formatada = data_atual.toLocaleDateString();
  return data_formatada;

}


function parseMonetaryValue(value) {
  return parseFloat(value.replace(/\./g, '').replace(',', '.'));
}


function carrega_dados_ranking_doctos_indefinidos(){
  $('#msg_erro').text("")
  $('#msg_erro').css('display','none')


  $.ajax({
    url: carrega_dados_ranking_docto_indefinido,
    type: 'POST',
    dataType: 'JSON',
    data: { "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val() },
    success: function (data) {
      //carrega_ranking(data.data);

    },
    error: function (error) {
        console.error('Erro na requisição:', error);
        $('#msg_erro').text("Estamos com instabilidade na conexão de clientes, por favor acionar a equipe responsável.")
        $('#msg_erro').css('display','block')
    }
});

}


$("#btn_filtro").on("click", function () {
  
  var range_datas = $("#flatpickr-range").val();
  var datas_formatadas = formata_range_datas(range_datas);
  
  $("#data_vencimento").text(datas_formatadas.data_inicial + " - " + datas_formatadas.data_final);

  retorna_dados_dash(datas_formatadas.data_inicial, datas_formatadas.data_final);
  recuperar_doctos_indefinidos(datas_formatadas.data_inicial, datas_formatadas.data_final);
  
  $("#btn_limpa_filtro").removeClass("d-none");
});


function pegar_data_filtro(data_formatada,data_formatada2) {
  // Converte a data formatada de 'DD/MM/YYYY' para 'YYYY-MM-DD'
  var partes = data_formatada.split('/');
  var data_convertida = partes[2] + '-' + partes[1] + '-' + partes[0];

  var partes = data_formatada2.split('/');
  var data_convertida2 = partes[2] + '-' + partes[1] + '-' + partes[0];

  // Define o valor no flatpickr
  $("#flatpickr-range").val(data_convertida + " to " + data_convertida2);

  return {
    data_inicial: data_convertida,
    data_final: data_convertida2
  };
}


function formata_range_datas(range_datas) {
  
  var datas = range_datas.split(" to ");
  
  var data_inicial = datas[0] ? formatDate(datas[0]) : '';
  var data_final = datas[1] ? formatDate(datas[1]) : '';

  if (!data_final) {
    data_final = data_inicial;
  }

  return {
    data_inicial: data_inicial,
    data_final: data_final
  };
}


// Função auxiliar para formatar a data
function formatDate(data) {
  var parts = data.split("-");
  return parts[2] + '/' + parts[1] + '/' + parts[0];
}


function recupera_dados_doctos_gerais(codigo){
  
  $('#msg_erro').text("")
  $('#msg_erro').css('display','none')
  console.log(codigo)
  var range_datas = $("#flatpickr-range").val();
  var datas_formatadas = formata_range_datas(range_datas);
        
  $.ajax({
    url: carrega_dados_doctos_gerais,
    type: 'POST',
    dataType: 'JSON',
    data: { "datini":datas_formatadas.data_inicial,"datfim":datas_formatadas.data_final,"codemp":codigo,"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val() },
    success: function (data) {
      carrega_lista_doctos_gerais(data.data.ListaCliente);
    },
    error: function (error) {
        console.error('Erro na requisição:', error);
        $('#msg_erro').text("Estamos com instabilidade na conexão de clientes, por favor acionar a equipe responsável.")
        $('#msg_erro').css('display','block')
    }
});

}


function carrega_lista_doctos_gerais(data) {
  const tbody = $('#ranking_lista_geral');
  tbody.empty();
  
  console.log(data)

  data.forEach((item, index) => {


    valor_formatado = formatarMoeda(parseFloat(item.Valor.toString().replace(".","").replace(",","")) /100)
   
    const row = `
      <tr>
              <td>
                <div class="d-flex align-items-center">
                  <span class="text-heading" style="color: ${item.Color} !important">${item.CodCli} - ${item.DescricaoEmpresa.substring(0,25)}</span>
                </div>
              </td>
              <!-- Dados de Demonstração de Documentos Indefinidos -->
              <td class="f-bold" style="color: ${item.Color} !important">${item.DataVencimento}</td>
              <td class="text-heading" style="color: ${item.Color} !important">${item.DescricaoFornecedor.substring(0,25)}</td>
              <td class="text-heading" style="color: ${item.Color} !important">${item.NumeroDocumento}</td>
              <td class="text-heading" style="color: ${item.Color} !important">${valor_formatado}</td>
              </td>        
            </tr>
    `;

    tbody.append(row);
  });

}