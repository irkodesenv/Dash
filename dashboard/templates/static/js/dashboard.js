  $(document).ready(function() {
    
        var data_formatada = data_atual();
        $("#data_vencimento").text(data_formatada);
        
        retorna_dados_dash();
        recuperar_doctos_indefinidos();
        //carrega_dados_ranking_doctos_indefinidos();

        setInterval(function() {        
          retorna_dados_dash();
          recuperar_doctos_indefinidos();
        }, 60000);


  })


//função para retornar dados dashboard
function retorna_dados_dash(){
  $('#msg_erro').text("")
  $('#msg_erro').css('display','none')


  $.ajax({
    url: carrega_dados_dash,
    type: 'POST',
    dataType: 'JSON',
    data: { "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val() },
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
function recuperar_doctos_indefinidos(){
  $('#msg_erro').text("")
  $('#msg_erro').css('display','none')

  $.ajax({
    url: carrega_dados_doctos_indefinidos,
    type: 'POST',
    dataType: 'JSON',
    data: { "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val() },
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

  top6.forEach((item, index) => {

    const valorItem = parseMonetaryValue(item.valortotal);
    const percentual = ((valorItem / data.Totais.TotalValor) * 100).toFixed(2);
    
    const logoPath = `/templates/static/media/logos_emp/${item.codigoempresa}.png`;
    const defaultLogo = '/templates/static/media/logos_emp/default.png';

    const row = `
      <tr>
        <td>${index + 1}</td>
        <td class="padding-left-0">
          <div class="d-flex align-items-center">
            <img src="${logoPath}" onerror="this.onerror=null;this.src='${defaultLogo}';" height="24" width="24" class="me-3" />
            <span class="text-heading">${item.razao}</span>
          </div>
        </td>
        <td class="text-heading">${item.quantidadedocumentos}</td>
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

    const row = `
      <tr>
        <td>${index + 9}</td>
        <td class="padding-left-0">
          <div class="d-flex align-items-center">
            <img src="${logoPath}" onerror="this.onerror=null;this.src='${defaultLogo}';" height="24" width="24" class="me-3" />
            <span class="text-heading">${item.razao}</span>
          </div>
        </td>
        <td class="text-heading">${item.quantidadedocumentos}</td>
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