"""Consolida a revisão humana de adequação semântica dos testes gerados.

A escala usada em cada eixo é: 0 = não atende, 1 = atende parcialmente e
2 = atende completamente. O arquivo não altera testes, prompts ou resultados
de execução; apenas lê os artefatos preservados e produz CSV/JSON/Markdown.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "python_app" / "avaliacao_prompts"
TESTS = ROOT / "python_app" / "teste_prompt_e2e_semantico" / "generated_tests"
OUTPUT = EVAL / "resultados_adequacao_semantica_20260728"


# model|round|scenario|condition|flow|target|assertion|review note
REVIEW_DATA = r"""
gpt-5.6-sol|gpt_original_12|suite_adicionar_carrinho|baseline|2|1|2|Fluxo e oráculo completos; o botão genérico Add to cart é ambíguo na página do produto.
gpt-5.6-sol|gpt_original_12|suite_adicionar_carrinho|structured_context|2|2|2|Fluxo completo e ID específico do produto; confirma notificação e item no carrinho.
gpt-5.6-sol|gpt_original_12|suite_busca_blue_jeans|baseline|2|2|2|Busca, abre o resultado correto e valida a página de detalhes.
gpt-5.6-sol|gpt_original_12|suite_busca_blue_jeans|structured_context|2|2|2|Busca, abre o resultado correto e valida URL, título e nome do produto.
gpt-5.6-sol|gpt_original_12|suite_checkout_blue_jeans|baseline|2|1|2|Cobre o checkout completo, mas o avanço presume controles visíveis no estado AJAX observado.
gpt-5.6-sol|gpt_original_12|suite_checkout_blue_jeans|structured_context|2|1|2|Cobre o checkout completo, mas presume visibilidade imediata dos contêineres de endereço.
gpt-5.6-sol|gpt_original_12|suite_configurar_desktop|baseline|2|1|2|Seleciona as quatro opções e valida o carrinho; labels exatos omitem os acréscimos de preço reais.
gpt-5.6-sol|gpt_original_12|suite_configurar_desktop|structured_context|2|1|2|Fluxo e opções completos; o escopo category-grid não correspondeu ao DOM observado.
gpt-5.6-sol|gpt_original_12|suite_detalhes_fiction|baseline|2|2|2|Localiza Fiction e valida nome e preço.
gpt-5.6-sol|gpt_original_12|suite_detalhes_fiction|structured_context|2|2|2|Localiza Fiction e valida nome e preço com alvos específicos.
gpt-5.6-sol|gpt_original_12|suite_limpar_carrinho|baseline|2|2|2|Prepara o carrinho, remove Blue Jeans e confirma o estado vazio.
gpt-5.6-sol|gpt_original_12|suite_limpar_carrinho|structured_context|2|2|2|Prepara o carrinho, remove Blue Jeans e confirma o estado vazio.
gpt-5.6-sol|gpt_original_12|suite_limpar_wishlist|baseline|2|1|2|Cobre autenticação, preparação, remoção e estado vazio; Add to wishlist resolve mais de um elemento.
gpt-5.6-sol|gpt_original_12|suite_limpar_wishlist|structured_context|2|1|2|Cobre autenticação, preparação, remoção e estado vazio; Add to wishlist permanece ambíguo.
gpt-5.6-sol|gpt_original_12|suite_login_invalido|baseline|2|2|2|Usa as credenciais do ambiente e valida mensagem e permanência sem autenticação.
gpt-5.6-sol|gpt_original_12|suite_login_invalido|structured_context|2|2|2|Usa as credenciais do ambiente e valida mensagem e permanência sem autenticação.
gpt-5.6-sol|gpt_original_12|suite_login_valido|baseline|2|2|2|Autentica e valida os controles de conta e encerramento de sessão.
gpt-5.6-sol|gpt_original_12|suite_login_valido|structured_context|2|2|2|Autentica e valida os controles de conta e encerramento de sessão.
gpt-5.6-sol|gpt_original_12|suite_logout|baseline|2|2|2|Parte de sessão autenticada, encerra-a e confirma o retorno de Log in.
gpt-5.6-sol|gpt_original_12|suite_logout|structured_context|2|2|2|Parte de sessão autenticada, encerra-a e confirma o retorno de Log in.
gpt-5.6-sol|gpt_original_12|suite_registro_usuario|baseline|2|2|2|Registra endereço único, confirma o cadastro e retorna autenticado.
gpt-5.6-sol|gpt_original_12|suite_registro_usuario|structured_context|2|1|2|Conclui e confirma o cadastro, mas trata Continue como link em vez de botão.
gpt-5.6-sol|gpt_original_12|suite_adicionar_wishlist|baseline|2|1|2|Representa autenticação, busca, inclusão e verificação; falha ao localizar a busca após login.
gpt-5.6-sol|gpt_original_12|suite_adicionar_wishlist|structured_context|2|1|2|Adiciona e recebe confirmação, mas o locator do item na wishlist não corresponde ao DOM.
qwen2.5-coder:7b|qwen_new_20|fluxo_computadores_desktops|baseline|1|1|1|Usa rota relativa e classe digital-item inventada; não comprova de modo confiável os itens disponíveis.
qwen2.5-coder:7b|qwen_new_20|fluxo_computadores_desktops|structured_context|1|2|1|Navega e valida a categoria correta, mas omite a verificação dos itens digitais.
qwen2.5-coder:7b|qwen_new_20|suite_adicionar_dois_produtos_carrinho|baseline|2|0|1|Representa a sequência em outra aplicação, com seletores e preços inventados e asserções web sem await.
qwen2.5-coder:7b|qwen_new_20|suite_adicionar_dois_produtos_carrinho|structured_context|0|1|1|Divide um único fluxo em quatro testes isolados e não adiciona Fiction ao carrinho; o estado não é compartilhado.
qwen2.5-coder:7b|qwen_new_20|suite_atualizar_quantidade_carrinho|baseline|2|0|1|Fluxo nominal presente, porém rotas e controles são inventados e o subtotal esperado é fixado arbitrariamente.
qwen2.5-coder:7b|qwen_new_20|suite_atualizar_quantidade_carrinho|structured_context|2|1|1|Usa o produto real, mas espera redirecionamento inexistente e compara o preço unitário ao total do pedido.
qwen2.5-coder:7b|qwen_new_20|suite_busca_sem_resultados|baseline|2|0|2|Fluxo e intenção do oráculo estão presentes, mas os controles e a mensagem pertencem a uma interface inventada.
qwen2.5-coder:7b|qwen_new_20|suite_busca_sem_resultados|structured_context|2|2|1|Busca corretamente um termo inexistente; a mensagem esperada não coincide com a resposta observada.
qwen2.5-coder:7b|qwen_new_20|suite_cadastro_campos_obrigatorios|baseline|2|1|0|Submete campos vazios, mas usa um único locator incompatível para cinco mensagens distintas.
qwen2.5-coder:7b|qwen_new_20|suite_cadastro_campos_obrigatorios|structured_context|2|2|1|Cobre os cinco campos e mensagens, mas a mensagem de senha resolve dois elementos e invalida o oráculo.
qwen2.5-coder:7b|qwen_new_20|suite_cadastro_confirmacao_senha|baseline|2|1|1|Cobre senhas divergentes com email único, mas IDs e texto de erro não correspondem à aplicação.
qwen2.5-coder:7b|qwen_new_20|suite_cadastro_confirmacao_senha|structured_context|2|2|1|Preenche os controles reais; a mensagem The specified passwords do not match não é a exibida.
qwen2.5-coder:7b|qwen_new_20|suite_cadastro_senha_curta|baseline|2|1|1|Representa a validação pedida, mas usa IDs e mensagem de outra interface.
qwen2.5-coder:7b|qwen_new_20|suite_cadastro_senha_curta|structured_context|2|2|0|Ações corretas, porém chama toHaveText sobre Page; não existe uma asserção executável do erro.
qwen2.5-coder:7b|qwen_new_20|suite_carrinho_inicialmente_vazio|baseline|2|0|1|Representa o estado vazio em rota e classes inexistentes.
qwen2.5-coder:7b|qwen_new_20|suite_carrinho_inicialmente_vazio|structured_context|2|2|1|Abre o carrinho real, mas não valida contagem zero e procura uma mensagem como heading inexistente.
qwen2.5-coder:7b|qwen_new_20|suite_comparar_produtos|baseline|2|1|1|Fluxo nominal correto, com IDs inventados e validação que não identifica os produtos pelo nome.
qwen2.5-coder:7b|qwen_new_20|suite_comparar_produtos|structured_context|1|1|1|Adiciona apenas o primeiro produto; clicar no texto Fiction não equivale a adicioná-lo à comparação.
qwen2.5-coder:7b|qwen_new_20|suite_enquete_sem_resposta|baseline|2|1|1|A intenção está correta, mas inventa navegação e um alerta inline diferente do controle real.
qwen2.5-coder:7b|qwen_new_20|suite_enquete_sem_resposta|structured_context|2|2|0|Clica no botão real, porém espera que ele fique desabilitado e usa toHaveText sobre Page.
qwen2.5-coder:7b|qwen_new_20|suite_exibir_quatro_livros|baseline|2|1|2|Seleciona quatro e conta produtos, mas o identificador do controle Display é inventado.
qwen2.5-coder:7b|qwen_new_20|suite_exibir_quatro_livros|structured_context|1|2|1|Não seleciona 4 no controle Display e exige exatamente quatro itens, não no máximo quatro.
qwen2.5-coder:7b|qwen_new_20|suite_filtrar_livros_abaixo_25|baseline|2|1|0|Aciona o filtro, mas o oráculo apenas procura a frase Over 25.00 e não inspeciona preços.
qwen2.5-coder:7b|qwen_new_20|suite_filtrar_livros_abaixo_25|structured_context|2|2|0|Navega e filtra corretamente, mas interpreta o texto do botão Add to cart como preço.
qwen2.5-coder:7b|qwen_new_20|suite_navegar_cartoes_presente|baseline|2|1|1|Navega para a categoria correta; os seletores de produtos e a forma exata do breadcrumb são incorretos.
qwen2.5-coder:7b|qwen_new_20|suite_navegar_cartoes_presente|structured_context|0|2|0|Fragmenta a navegação em testes independentes e valida apenas o heading, sem breadcrumb ou produtos.
qwen2.5-coder:7b|qwen_new_20|suite_navegar_categoria_livros|baseline|2|1|2|Nomes corretos e oráculo completo, mas classes e contagem rígida não correspondem ao catálogo.
qwen2.5-coder:7b|qwen_new_20|suite_navegar_categoria_livros|structured_context|2|2|1|Fluxo e produtos corretos, porém todas as expectativas assíncronas estão sem await.
qwen2.5-coder:7b|qwen_new_20|suite_navegar_sobre_nos|baseline|2|0|2|Intenção e heading presentes, mas o domínio e a interação com a seção Information são inventados.
qwen2.5-coder:7b|qwen_new_20|suite_navegar_sobre_nos|structured_context|2|2|1|Navega corretamente até About us, mas não verifica o heading solicitado.
qwen2.5-coder:7b|qwen_new_20|suite_ordenar_livros_por_preco|baseline|2|1|2|Compara preços em ordem, mas modela o seletor de ordenação e a classe de preço incorretamente.
qwen2.5-coder:7b|qwen_new_20|suite_ordenar_livros_por_preco|structured_context|2|1|2|Oráculo matemático adequado; tenta acionar a ordenação como botão, não como combobox.
qwen2.5-coder:7b|qwen_new_20|suite_persistencia_carrinho_apos_login|baseline|1|0|1|Usa outra aplicação, não importa Page e não implementa corretamente o novo login após logout.
qwen2.5-coder:7b|qwen_new_20|suite_persistencia_carrinho_apos_login|structured_context|0|1|1|Não limpa o estado inicial nem faz logout; tenta abrir Log in enquanto a sessão continua autenticada.
qwen2.5-coder:7b|qwen_new_20|suite_produtos_visualizados_recentemente|baseline|2|0|2|Representa a ordem pedida, mas usa outra aplicação e seletores inventados.
qwen2.5-coder:7b|qwen_new_20|suite_produtos_visualizados_recentemente|structured_context|1|2|1|Abre apenas Blue Jeans; Fiction depende indevidamente de histórico anterior em contexto novo.
qwen2.5-coder:7b|qwen_new_20|suite_visualizacao_livros_em_lista|baseline|2|1|1|Expressa a troca Grid para List, mas usa controles inventados e expectativas sem await.
qwen2.5-coder:7b|qwen_new_20|suite_visualizacao_livros_em_lista|structured_context|1|1|0|Procura um botão opcional em vez do controle View as e nunca comprova a visualização em lista.
qwen2.5-coder:7b|qwen_new_20|user_registration_book_purchase|baseline|2|1|0|Cobre o fluxo nominal, mas reutiliza email, espera rota falsa e possui asserções booleanas inertes.
qwen2.5-coder:7b|qwen_new_20|user_registration_book_purchase|structured_context|2|2|0|Usa os controles reais, porém todas as expectativas web estão sem await e o email fixo interfere em reexecuções.
gemini-3.6-flash|gemini_new_20|fluxo_computadores_desktops|baseline|2|1|2|Fluxo e oráculo completos, mas o domínio padrão é outra instalação nopCommerce.
gemini-3.6-flash|gemini_new_20|fluxo_computadores_desktops|structured_context|2|2|2|Navega, valida página e comprova a existência de itens digitais.
gemini-3.6-flash|gemini_new_20|suite_adicionar_dois_produtos_carrinho|baseline|2|2|2|Adiciona os dois livros no mesmo teste e valida linhas, quantidade e preços.
gemini-3.6-flash|gemini_new_20|suite_adicionar_dois_produtos_carrinho|structured_context|2|2|1|Adiciona e valida os dois produtos, mas não verifica quantidade e preço de cada linha.
gemini-3.6-flash|gemini_new_20|suite_atualizar_quantidade_carrinho|baseline|2|1|2|Fluxo e cálculo completos; o domínio padrão é outra instalação nopCommerce.
gemini-3.6-flash|gemini_new_20|suite_atualizar_quantidade_carrinho|structured_context|2|2|2|Atualiza quantidade e compara subtotal da linha com duas vezes o preço unitário.
gemini-3.6-flash|gemini_new_20|suite_busca_sem_resultados|baseline|2|1|2|Usa termo único e valida a ausência de resultados, mas aponta por padrão para outra instalação.
gemini-3.6-flash|gemini_new_20|suite_busca_sem_resultados|structured_context|2|2|2|Executa a busca real e valida a mensagem de ausência de produtos.
gemini-3.6-flash|gemini_new_20|suite_cadastro_campos_obrigatorios|baseline|2|2|2|Valida as cinco ocorrências e distingue as duas mensagens iguais de senha.
gemini-3.6-flash|gemini_new_20|suite_cadastro_campos_obrigatorios|structured_context|2|2|2|Valida permanência na página, cinco erros e os textos correspondentes.
gemini-3.6-flash|gemini_new_20|suite_cadastro_confirmacao_senha|baseline|2|2|2|Usa email único, senhas divergentes e valida erro e ausência de navegação.
gemini-3.6-flash|gemini_new_20|suite_cadastro_confirmacao_senha|structured_context|2|2|2|Usa os controles reais e a mensagem efetivamente apresentada pela aplicação.
gemini-3.6-flash|gemini_new_20|suite_cadastro_senha_curta|baseline|2|1|2|Cobre a validação pedida, mas usa localhost como destino padrão.
gemini-3.6-flash|gemini_new_20|suite_cadastro_senha_curta|structured_context|2|2|2|Usa senha de cinco caracteres e confirma a mensagem de validação.
gemini-3.6-flash|gemini_new_20|suite_carrinho_inicialmente_vazio|baseline|2|0|2|Oráculo completo, porém executa por padrão contra um domínio de comércio inventado.
gemini-3.6-flash|gemini_new_20|suite_carrinho_inicialmente_vazio|structured_context|2|2|1|Confirma página e mensagem de carrinho vazio, mas omite a contagem zero solicitada.
gemini-3.6-flash|gemini_new_20|suite_comparar_produtos|baseline|2|2|2|Adiciona os dois produtos, valida ambos e limpa a lista.
gemini-3.6-flash|gemini_new_20|suite_comparar_produtos|structured_context|2|2|2|Adiciona os dois produtos no mesmo fluxo, valida-os e limpa a lista.
gemini-3.6-flash|gemini_new_20|suite_enquete_sem_resposta|baseline|2|2|2|Não seleciona resposta e trata tanto diálogo quanto mensagem inline.
gemini-3.6-flash|gemini_new_20|suite_enquete_sem_resposta|structured_context|2|2|2|Usa o botão e o contêiner de erro reais e valida a mensagem.
gemini-3.6-flash|gemini_new_20|suite_exibir_quatro_livros|baseline|2|2|2|Seleciona 4, mantém Books visível e valida limite e presença de produtos.
gemini-3.6-flash|gemini_new_20|suite_exibir_quatro_livros|structured_context|2|2|2|Seleciona o controle real e valida de um a quatro produtos.
gemini-3.6-flash|gemini_new_20|suite_filtrar_livros_abaixo_25|baseline|2|0|2|O arquivo cria um DOM simulado quando BASE_URL não é fornecida; além disso contém erro de sintaxe e não testa a aplicação alvo.
gemini-3.6-flash|gemini_new_20|suite_filtrar_livros_abaixo_25|structured_context|2|2|2|Aplica o filtro real e verifica numericamente todos os preços exibidos.
gemini-3.6-flash|gemini_new_20|suite_navegar_cartoes_presente|baseline|2|2|2|Valida rota, heading, breadcrumb e presença de produtos.
gemini-3.6-flash|gemini_new_20|suite_navegar_cartoes_presente|structured_context|2|2|2|Valida rota, heading, breadcrumb e presença de produtos.
gemini-3.6-flash|gemini_new_20|suite_navegar_categoria_livros|baseline|2|2|2|Valida página, breadcrumb e os três livros solicitados.
gemini-3.6-flash|gemini_new_20|suite_navegar_categoria_livros|structured_context|2|2|2|Valida página, breadcrumb e os três livros solicitados.
gemini-3.6-flash|gemini_new_20|suite_navegar_sobre_nos|baseline|2|2|2|Restringe About us ao rodapé e valida URL e heading.
gemini-3.6-flash|gemini_new_20|suite_navegar_sobre_nos|structured_context|2|2|2|Navega e valida URL e heading; não restringe o link ao rodapé, mas aciona o alvo correto.
gemini-3.6-flash|gemini_new_20|suite_ordenar_livros_por_preco|baseline|2|2|2|Seleciona o combobox e verifica numericamente ordem não decrescente.
gemini-3.6-flash|gemini_new_20|suite_ordenar_livros_por_preco|structured_context|2|2|2|Seleciona o combobox e verifica numericamente ordem não decrescente.
gemini-3.6-flash|gemini_new_20|suite_persistencia_carrinho_apos_login|baseline|2|2|2|Usa credenciais do ambiente, limpa o estado, reloga, verifica persistência e restaura a conta em finally.
gemini-3.6-flash|gemini_new_20|suite_persistencia_carrinho_apos_login|structured_context|2|2|2|Limpa o estado, adiciona o produto, reloga, confirma persistência e remove o item ao final.
gemini-3.6-flash|gemini_new_20|suite_produtos_visualizados_recentemente|baseline|2|1|2|Fluxo e ordem completos, mas o domínio padrão é outra instalação nopCommerce.
gemini-3.6-flash|gemini_new_20|suite_produtos_visualizados_recentemente|structured_context|2|2|2|Abre Fiction e depois Blue Jeans, valida presença e ordem relativa.
gemini-3.6-flash|gemini_new_20|suite_visualizacao_livros_em_lista|baseline|2|2|1|Seleciona List e verifica o valor do controle, mas aceita também um contêiner de grid como prova da visualização.
gemini-3.6-flash|gemini_new_20|suite_visualizacao_livros_em_lista|structured_context|2|2|2|Seleciona List no controle real e comprova o contêiner product-list.
gemini-3.6-flash|gemini_new_20|user_registration_book_purchase|baseline|2|2|2|Usa email único e valida registro, sessão, catálogo, produto, notificação e carrinho.
gemini-3.6-flash|gemini_new_20|user_registration_book_purchase|structured_context|2|2|2|Valida todas as etapas principais do registro até a presença de Health Book no carrinho.
""".strip()


GPT_EXECUTION = {
    "suite_adicionar_carrinho": ("failed", "passed"),
    "suite_busca_blue_jeans": ("passed", "passed"),
    "suite_checkout_blue_jeans": ("failed", "failed"),
    "suite_configurar_desktop": ("failed", "failed"),
    "suite_detalhes_fiction": ("passed", "passed"),
    "suite_limpar_carrinho": ("passed", "passed"),
    "suite_limpar_wishlist": ("failed", "failed"),
    "suite_login_invalido": ("passed", "passed"),
    "suite_login_valido": ("passed", "passed"),
    "suite_logout": ("passed", "passed"),
    "suite_registro_usuario": ("passed", "failed"),
    "suite_adicionar_wishlist": ("failed", "failed"),
}


def classification(total: int) -> str:
    if total == 6:
        return "adequate"
    if total >= 3:
        return "partially_adequate"
    return "inadequate"


def playwright_statuses(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    blocks: dict[str, list[str]] = defaultdict(list)

    def visit(suite: dict) -> None:
        filename = Path(suite.get("file", "")).stem.replace(".spec", "")
        for spec in suite.get("specs", []):
            for test in spec.get("tests", []):
                results = test.get("results", [])
                status = results[-1].get("status", "not_run") if results else "not_run"
                blocks[filename].append(status)
        for child in suite.get("suites", []):
            visit(child)

    for suite in data.get("suites", []):
        visit(suite)

    return {
        scenario: "passed" if values and all(v == "passed" for v in values) else "failed"
        for scenario, values in blocks.items()
    }


def source_path(model: str, round_id: str, scenario: str, condition: str) -> Path:
    if round_id == "gpt_original_12":
        aliases = {
            "suite_busca_blue_jeans": "buscar_blue_jeans",
            "suite_adicionar_wishlist": "wishlist",
        }
        short = aliases.get(scenario, scenario.removeprefix("suite_"))
        suffix = "baseline" if condition == "baseline" else "estruturado"
        return (
            TESTS
            / "archive_before_qwen25coder_gpu_20260724_01"
            / condition
            / f"teste_{short}_{suffix}.spec.ts"
        )
    directories = {
        ("qwen_old_14", "baseline"): "baseline_playwright_locators_20260724_02",
        ("qwen_old_14", "structured_context"): "structured_context_playwright_locators_20260724_02",
        ("qwen_new_20", "baseline"): "baseline_qwen25coder_demowebshop20_20260727_01",
        ("qwen_new_20", "structured_context"): "structured_context_qwen25coder_demowebshop20_20260727_01",
        ("gemini_new_20", "baseline"): "baseline_gemini36flash_demowebshop20_20260727_01",
        ("gemini_new_20", "structured_context"): "structured_context_gemini36flash_demowebshop20_20260727_01",
    }
    return TESTS / directories[(round_id, condition)] / f"{scenario}.spec.ts"


def load_rows() -> list[dict]:
    qwen_new_baseline = playwright_statuses(
        EVAL / "resultados_qwen25coder_demowebshop20_20260727_01" / "baseline.playwright.json"
    )
    qwen_new_structured = playwright_statuses(
        EVAL
        / "resultados_qwen25coder_demowebshop20_20260727_01"
        / "structured_context.playwright.json"
    )
    gemini_baseline = playwright_statuses(
        EVAL
        / "resultados_gemini36flash_demowebshop20_20260728_01"
        / "baseline.executable_subset.playwright.json"
    )
    gemini_baseline["suite_filtrar_livros_abaixo_25"] = "syntax_error"
    gemini_structured = playwright_statuses(
        EVAL
        / "resultados_gemini36flash_demowebshop20_20260728_01"
        / "structured_context.playwright.json"
    )

    execution_maps = {
        ("qwen_new_20", "baseline"): qwen_new_baseline,
        ("qwen_new_20", "structured_context"): qwen_new_structured,
        ("gemini_new_20", "baseline"): gemini_baseline,
        ("gemini_new_20", "structured_context"): gemini_structured,
    }
    rows: list[dict] = []

    for line in REVIEW_DATA.splitlines():
        model, round_id, scenario, condition, flow, target, assertion, note = line.split("|", 7)
        if round_id == "gpt_original_12":
            execution = GPT_EXECUTION[scenario][0 if condition == "baseline" else 1]
        else:
            execution = execution_maps[(round_id, condition)].get(scenario, "not_run")
        total = int(flow) + int(target) + int(assertion)
        path = source_path(model, round_id, scenario, condition)
        if not path.is_file():
            raise FileNotFoundError(path)
        rows.append(
            {
                "model": model,
                "round": round_id,
                "scenario": scenario,
                "condition": condition,
                "execution_status": execution,
                "flow_correctness": int(flow),
                "target_correctness": int(target),
                "assertion_correctness": int(assertion),
                "semantic_total_6": total,
                "semantic_classification": classification(total),
                "source_file": str(path.relative_to(ROOT)),
                "review_note": note,
            }
        )

    old_path = EVAL / "resultados_qwen_playwright_locators_20260724_02" / "human_review.csv"
    with old_path.open(encoding="utf-8", newline="") as handle:
        for old in csv.DictReader(handle):
            scores = [int(old[key]) for key in (
                "flow_correctness",
                "target_correctness",
                "assertion_correctness",
            )]
            total = sum(scores)
            path = source_path(
                "qwen2.5-coder:7b", "qwen_old_14", old["spec_id"], old["approach"]
            )
            if not path.is_file():
                raise FileNotFoundError(path)
            rows.append(
                {
                    "model": "qwen2.5-coder:7b",
                    "round": "qwen_old_14",
                    "scenario": old["spec_id"],
                    "condition": old["approach"],
                    "execution_status": old["execution_status"],
                    "flow_correctness": scores[0],
                    "target_correctness": scores[1],
                    "assertion_correctness": scores[2],
                    "semantic_total_6": total,
                    "semantic_classification": classification(total),
                    "source_file": str(path.relative_to(ROOT)),
                    "review_note": old["justification"],
                }
            )
    return sorted(rows, key=lambda row: (
        row["model"], row["round"], row["scenario"], row["condition"]
    ))


def summarize(rows: list[dict]) -> dict:
    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["model"], row["round"], row["condition"])].append(row)

    conditions = []
    for (model, round_id, condition), items in sorted(grouped.items()):
        counts = defaultdict(int)
        for item in items:
            counts[item["semantic_classification"]] += 1
        conditions.append(
            {
                "model": model,
                "round": round_id,
                "condition": condition,
                "files": len(items),
                "adequate": counts["adequate"],
                "partially_adequate": counts["partially_adequate"],
                "inadequate": counts["inadequate"],
                "adequacy_rate": round(counts["adequate"] / len(items), 4),
                "mean_semantic_score_6": round(
                    sum(item["semantic_total_6"] for item in items) / len(items), 3
                ),
                "execution_passed": sum(
                    item["execution_status"] == "passed" for item in items
                ),
                "syntax_errors": sum(
                    item["execution_status"] == "syntax_error" for item in items
                ),
            }
        )

    paired = []
    by_round: dict[tuple[str, str], dict[str, dict[str, dict]]] = defaultdict(
        lambda: defaultdict(dict)
    )
    for row in rows:
        by_round[(row["model"], row["round"])][row["condition"]][row["scenario"]] = row
    for (model, round_id), approaches in sorted(by_round.items()):
        baseline = approaches["baseline"]
        structured = approaches["structured_context"]
        common = sorted(set(baseline) & set(structured))
        deltas = [
            structured[scenario]["semantic_total_6"]
            - baseline[scenario]["semantic_total_6"]
            for scenario in common
        ]
        paired.append(
            {
                "model": model,
                "round": round_id,
                "pairs": len(common),
                "structured_improved": sum(delta > 0 for delta in deltas),
                "same_score": sum(delta == 0 for delta in deltas),
                "structured_worsened": sum(delta < 0 for delta in deltas),
                "mean_score_delta": round(sum(deltas) / len(deltas), 3),
            }
        )
    return {"total_files": len(rows), "conditions": conditions, "paired_comparison": paired}


def write_markdown(summary: dict) -> None:
    lines = [
        "# Avaliação de adequação semântica",
        "",
        "A unidade é o arquivo gerado comparado à respectiva especificação em linguagem natural.",
        "Aprovação em execução e adequação semântica são registradas separadamente.",
        "",
        "## Rubrica",
        "",
        "- fluxo: presença e coerência das etapas e pré-condições pedidas;",
        "- alvo: aplicação, dados, produtos e controles corretos;",
        "- asserção: capacidade de comprovar todos os resultados solicitados.",
        "",
        "Cada eixo recebe 0 (não atende), 1 (parcial) ou 2 (completo). Um arquivo é",
        "**adequado** somente com 6/6; **parcialmente adequado** com 3–5; e",
        "**inadequado** com 0–2. Uma expectativa assíncrona sem `await`, um teste",
        "fragmentado que depende de outro contexto ou um DOM simulado não recebe",
        "crédito integral.",
        "",
        "## Resultado por condição",
        "",
        "| Modelo | Rodada | Condição | Arquivos | Adequados | Parciais | Inadequados | Média / 6 | Passaram | Erro de sintaxe |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in summary["conditions"]:
        lines.append(
            f"| {item['model']} | {item['round']} | {item['condition']} | "
            f"{item['files']} | {item['adequate']} | {item['partially_adequate']} | "
            f"{item['inadequate']} | {item['mean_semantic_score_6']:.3f} | "
            f"{item['execution_passed']} | {item['syntax_errors']} |"
        )
    lines += [
        "",
        "## Comparação pareada da nota semântica",
        "",
        "| Modelo | Rodada | Pares | Estruturado melhor | Mesma nota | Estruturado pior | Delta médio / 6 |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in summary["paired_comparison"]:
        lines.append(
            f"| {item['model']} | {item['round']} | {item['pairs']} | "
            f"{item['structured_improved']} | {item['same_score']} | "
            f"{item['structured_worsened']} | {item['mean_score_delta']:+.3f} |"
        )
    lines += [
        "",
        "## Leitura comparativa",
        "",
        "- No Gemini, o contexto estruturado elevou os testes adequados de 12/20",
        "  para 18/20 e as aprovações de execução de 8/20 para 12/20. A única",
        "  piora semântica foi a omissão de quantidade e preço no cenário com dois",
        "  produtos no carrinho.",
        "- No GPT-5.6 Sol, as duas condições ficaram com 7/12 testes adequados e",
        "  média 5,583/6. O contexto corrigiu a ambiguidade de Add to cart, mas",
        "  introduziu o papel incorreto para Continue no registro.",
        "- No Qwen, o contexto aumentou a média nas duas rodadas, mas nenhum arquivo",
        "  alcançou os três eixos completos. Na rodada nova, a média passou de",
        "  3,700 para 3,900 e houve 9 melhorias, 6 empates e 5 pioras.",
        "- Aprovação em execução não implica conformidade integral: o Qwen",
        "  estruturado de Digital downloads passou sem verificar os itens, e o",
        "  Gemini estruturado de dois produtos passou sem verificar quantidade e",
        "  preço. O inverso também ocorre quando o fluxo é semanticamente próximo,",
        "  mas um locator ou papel incorreto impede a execução.",
        "- Os principais defeitos semânticos observados foram aplicação ou DOM",
        "  inventados, pré-condições omitidas, fragmentação de um fluxo em testes",
        "  sem estado compartilhado, asserções assíncronas sem await e oráculos que",
        "  verificam apenas parte do resultado solicitado.",
        "",
        "## Observações de escopo",
        "",
        "- A rodada Qwen antiga é a rodada corrigida de 14 pares; a rodada anterior",
        "  superseded não foi contada novamente.",
        "- O baseline Gemini possui um arquivo com erro de sintaxe. Para não impedir",
        "  a coleta dos demais, os outros 19 foram executados em uma cópia isolada.",
        "- Os arquivos originais não foram modificados e cada condição foi executada",
        "  em processo separado, com um worker e novo contexto por teste.",
        "",
        "A justificativa individual de cada nota está em `semantic_review.csv`.",
        "",
    ]
    (OUTPUT / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    fields = list(rows[0])
    with (OUTPUT / "semantic_review.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    summary = summarize(rows)
    (OUTPUT / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    write_markdown(summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
