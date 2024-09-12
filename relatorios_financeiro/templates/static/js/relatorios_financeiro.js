
$(document).ready(function() {
    // Select2 Country
    const arr_select = ["#select-clientes", "#select-usuarios", "#select-operadores"];

    for (let i = 0; i < arr_select.length; i++) {
        let selector = arr_select[i];
        let $selectElement = $(selector);
        
        if ($selectElement.length) {
          $selectElement.each(function () {
            let $this = $(this);
            $this.wrap('<div class="position-relative"></div>').select2({
              placeholder: 'Selecione',
              dropdownParent: $this.parent()
            });
          });
        }
      }
})


function limparSelectOperadores() {
  $('#select-operadores').val(null).trigger('change');
}


function retorna_operadores(codigo){

  if(codigo){
    $("#btn_operadores").removeClass('d-none')
  }else{
    $("#btn_operadores").addClass('d-none')
  }

  $.ajax({
    url: operadores,
    type: 'POST',
    dataType: 'JSON',
    data: { 
        "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(), 
        "codigo": codigo
    },
    success: function(data) {
        const tbody = $('.table-border-bottom-0');
        tbody.empty(); // Limpa a tabela antes de preencher

        data.forEach(usuario => {
            usuario.bancos.forEach(banco => {
                let flgMasterBadge = banco.FlgMaster === "S" ? '<span class="badge bg-label-success"> Sim </span>' : '<span class="badge bg-label-danger"> Não </span>';
                let nexxceraBadge = banco.Nexxcera === "1" ? '<span class="badge bg-label-success"> Sim </span>' : '<span class="badge bg-label-danger"> Não </span>';

                let row = `
                    <tr>
                      <td>
                        <div class="d-flex justify-content-start align-items-center">
                          <div class="avatar-wrapper">
                            <div class="avatar avatar-sm me-2">
                              <span class="avatar-initial rounded-circle bg-label-warning">${usuario.iniciais}</span>
                            </div>
                          </div>
                          <div class="d-flex flex-column">
                            <a href="pages-profile-user.html" class="text-heading text-truncate fw-medium">${usuario.nome}</a>
                            <small class="text-truncate text-body">${usuario.id_usuario}</small>
                          </div>
                        </div>
                      </td>
                      <td>${banco.DtaProcuracao}</td>
                      <td>${banco.CodigoOperador}</td>
                      <td>${flgMasterBadge}</td>
                      <td class="text-center padding-right-10 padding-left-10">
                        <img src="/templates/static/media/bancos/${banco.Banco}.png" class="img-fluid" width="20" />
                        <span style="margin-top: 3px !important">${banco.Banco}</span>
                      </td>
                      <td class="text-center">${banco.Agencia}</td>
                      <td class="text-center">${banco.ContaCorrente}</td>
                      <td>${nexxceraBadge}</td>
                      <td>${banco.CodCli} - ${banco.RazaoSocial}</td>
                    </tr>
                `;
                tbody.append(row);
            });
        });
    },
    error: function(error) {
        console.error('Erro ao obter operadores:', error);
    }
  });
}