
    $( document ).ready(function() {
        adicionar_loading("#volumetria_folha")
        adicionar_loading("#volumetria_financeiro")

        var cliente = $("#cliente").val();

        if(cliente){
            obter_descendentes(cliente);
        }   

        obter_volumetria_folha();
        obter_volumetria_contabil();
        obter_volumetria_financeiro();
    });


    function filtro(){
       return propriedades = {
            "cliente": $("#cliente").val(),
            "descendentes": $("#descendentes").val(),
            "pick_realizado": $("#pick_realizado").val(),
            "pick_comparativo": $("#pick_comparativo").val(),
            "demonstracao": $("#demonstracao").val()
       }
    }


    function obter_volumetria_folha(){
        adicionar_loading("#volumetria_folha")
        $.ajax({
            url: folha,
            type: 'POST',
            dataType: 'JSON',
            data: { 
                "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(), "filtro": filtro(), 
            },
            success: function(data) {                
                var tbody = $("#volumetria_folha");                  
                escreve_dados_no_quadro(tbody, data)
            },
            error: function(error) {
                console.error('Erro ao obter contas:', error);
            }
        });
    }


    function obter_volumetria_financeiro(){
        adicionar_loading("#volumetria_financeiro")
        $.ajax({
            url: financeiro,
            type: 'POST',
            dataType: 'JSON',
            data: { 
                "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(), "filtro": filtro(), 
            },
            success: function(data) {
                var tbody = $("#volumetria_financeiro");                  
                escreve_dados_no_quadro(tbody, data)
            },
            error: function(error) {
                console.error('Erro ao obter contas:', error);
            }
        });
    }


    function obter_volumetria_contabil(){
        adicionar_loading("#volumetria_contabil")       
        $.ajax({
            url: contabil,
            type: 'POST',
            dataType: 'JSON',
            data: { 
                "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(), "filtro": filtro(), 
            },
            success: function(data) {
                var tbody = $("#volumetria_contabil");          
                escreve_dados_no_quadro(tbody, data)
            },
            error: function(error) {
                console.error('Erro ao obter contas:', error);
            }
        });
    }


    function adicionar_loading(quadro){
        tbody = $(quadro);
        tbody.empty();

        loading = `
            <tr><td>.</td></tr>
            <tr><td></td></tr>
            <tr><td></td></tr>
            <tr>                                       
                <td colspan="6">
                    <div class="d-flex justify-content-center align-items-center" id="loading_folha" style="height: 25px;">
                        <!-- Fold -->
                        <div class="sk-fold sk-primary">
                            <div class="sk-fold-cube"></div>
                            <div class="sk-fold-cube"></div>
                            <div class="sk-fold-cube"></div>
                            <div class="sk-fold-cube"></div>
                        </div>
                    </div>
                </td>                                    
            </tr>
        `
        tbody.append(loading);
    }


    function remover_loading(quadro){
        var loading = $(quadro);
        loading.removeClass("d-flex").addClass("d-none");
    }


    $('#btn-filtrar').on('click', function (e) {
        obter_volumetria_financeiro();
        obter_volumetria_contabil();
        obter_volumetria_folha();
    });


    $('#cliente').on('change', function (e) {
        obter_descendentes(e.target.value);
    });


    function obter_descendentes(cliente){
        $.ajax({
            url: descendentes,
            type: 'POST',
            dataType: 'JSON',
            data: { 
                "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(), "cliente": cliente, 
            },
            success: function(data) {
                const select_descendentes = $("#descendentes");

                if(data.length > 0){
                    select_descendentes.empty();
                    select_descendentes.append("<option value=''> TODOS DESCENDENTES  </option>");

                    data.forEach(filialItem => {
                        select_descendentes.append("<option value='"+ filialItem.Codigo + "'>" + filialItem.Codigo + " - " + filialItem.Razao + "</option>");
                    });
                }else{
                    select_descendentes.empty();
                    select_descendentes.append("<option value=''> NÃO POSSUI </option>");
                }
            },
            error: function(error) {
                console.error('Erro ao obter contas:', error);
            }
        });
    }


    function escreve_dados_no_quadro(tbody, data){
        copia_tbody = tbody;
        // Limpar dados
        copia_tbody.empty()
        Object.entries(data).forEach(([key, value]) => {
            const linha = `
                <tr>
                    <td class='td-table-volumetria-left'>${key}</td>
                    
                    <td class='td-table-volumetria-center'>${value.orcado}</td>
    
                    <td class='td-table-volumetria-center'>${value.realizado}</td>

                    <td class="td-table-volumetria-center">
                        <div class="td-table-volumetria-center-percent">
                            <span>
                                ${value.realizado}
                            </span>
                                            
                            <span>                                                                           
                                ${
                                    value.percent > 0 
                                    ? `<small class="text-success fw-medium">                                                                        
                                            ${value.percent}%                                                
                                            <i class="bx bx-up-arrow-alt"></i>
                                        </small>`
                                    : value.percent < 0
                                    ? `<small class="text-danger fw-medium">                                                                       
                                            ${value.percent}%                                                
                                            <i class="bx bx-down-arrow-alt"></i>
                                        </small>`
                                    : `<small class="text-warning fw-medium">                                                                        
                                            0%                                                
                                            <i class="bx bx-right-arrow-alt"></i>
                                        </small>`
                                }                                                            
                            </span>
                        </div>
                    </td> 

                    <td class="td-table-volumetria-center"> ${value.comparativo}</td>   
                    
                    <td class="td-table-volumetria-center">
                        <div class="td-table-volumetria-center-percent">
                            <span>
                                ${value.realizado_x_comparativo}
                            </span>
                                            
                            <span>                                                                           
                                ${
                                    value.percent_rc > 0 
                                    ? `<small class="text-success fw-medium">                                                                        
                                            ${value.percent_rc}%                                                
                                            <i class="bx bx-up-arrow-alt"></i>
                                        </small>`
                                    : value.percent_rc < 0
                                    ? `<small class="text-danger fw-medium">                                                                       
                                            ${value.percent_rc}%                                                
                                            <i class="bx bx-down-arrow-alt"></i>
                                        </small>`
                                    : `<small class="text-warning fw-medium">                                                                        
                                            0%                                                
                                            <i class="bx bx-right-arrow-alt"></i>
                                        </small>`
                                }                                                            
                            </span>
                        </div>
                    </td> 
                </tr>
            `
            copia_tbody.append(linha);
        });
    }