from django.urls import path

from . import views
from . import viewsPF
from . import viewsPJ
from . import viewGerentePF
from . import viewGerentePJ
from . import viewAgencia

# modulo responsável pelas rotas da aplicação

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    
    
    # Pessoa Fisica
    path("registrar_pessoa_fisica", viewsPF.registrarPF, name="registrarPF"),
    path("fazerdepositoPF", viewsPF.fazerdepositoPF, name="fazerdepositoPF"),
    path("fazersaquePF", viewsPF.fazersaquePF, name="fazersaquePF"),
    path("acoes", viewsPF.acoes, name="acoes"),
    path("transferenciaPFparaPJ", viewsPF.transferenciaPFparaPJ, name="transferenciaPFparaPJ"),
    path("transferenciaPFparaPF", viewsPF.transferenciaPFparaPF, name="transferenciaPFparaPF"),
    path("historicoacoes", viewsPF.historicoacoes, name="historicoacoes"),
    path("historicotransferenciasPF", viewsPF.historicotransferencias, name="historicotransferenciasPF"),
    path("historicotransferenciasPJ", viewsPJ.historicotransferencias, name="historicotransferenciasPJ"),
    path("emprestimoparaPF", viewsPF.fazerEmprestimo, name="emprestimoparaPF"),
    path("mostrarHistoricoEmprestimos", viewsPF.mostrarHistoricoEmprestimos, name="mostrarHistoricoEmprestimos"),
    
    # Pessoa Juridica
    path("registrar_pessoa_juridica", viewsPJ.registrarPJ, name="registrarPJ"),
    path("fazerdepositoPJ", viewsPJ.fazerdepositoPJ, name="fazerdepositoPJ"),
    path("fazersaquePJ", views.fazersaquePJ, name="fazersaquePJ"),
    path("transferenciaPJparaPF", viewsPJ.transferenciaPJparaPF, name="transferenciaPJparaPF"),
    path("transferenciaPJparaPJ", viewsPJ.transferenciaPJparaPJ, name="transferenciaPJparaPJ"),
    
    # Gerente PF
    path("changePF", viewGerentePF.changePF, name="atualizarPF"),
    path("removePF", viewGerentePF.removePF, name="removePF"),
    path("renegociarEmprestimoPF", viewGerentePF.renegociarEmprestimoPF, name="renegociarEmprestimoPF"),
    
    # Gerente PJ
    path("changePJ", viewGerentePJ.changePJ, name="atualizarPJ"),
    path("removePJ", viewGerentePJ.removePJ, name="removePJ"),
    
    # Agencia
    path("alterarGerentes", viewAgencia.alterarGerentes, name="alterarGerentes"),
    path("deletarGerentes", viewAgencia.deletarGerentes, name="deletarGerentes"),
    path("registrarGerentePF", viewAgencia.registrarGerentesPF, name="registrarGerentePF"),
    path("mostrarClientes", viewAgencia.mostrarClientes, name="mostrarClientes")
]
