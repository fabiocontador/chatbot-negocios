from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def gerar_grafico(viabilidade):
    """Gera um gráfico de pizza e retorna como base64"""
    fig, ax = plt.subplots(figsize=(6, 4))
    labels = ['Viabilidade', 'Risco']
    sizes = [viabilidade, 100 - viabilidade]
    colors = ['#27ae60', '#e74c3c']
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')  # Garante que o gráfico seja circular

    # Salva a imagem em memória
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()  # Fecha a figura para liberar memória
    img.seek(0)

    # Codifica para base64
    grafico_url = base64.b64encode(img.getvalue()).decode()
    return f"data:image/png;base64,{grafico_url}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Coleta respostas
        concorrencia = request.form.get("concorrencia")
        clientes = request.form.get("clientes")
        marketing = request.form.get("marketing")
        estrutura = request.form.get("estrutura")
        financeiro = request.form.get("financeiro")

        # Coleta opções marcadas
        conc_opcoes = request.form.getlist("conc_opcoes")
        clientes_opcoes = request.form.getlist("clientes_opcoes")
        marketing_opcoes = request.form.getlist("marketing_opcoes")
        estrutura_opcoes = request.form.getlist("estrutura_opcoes")
        financeiro_opcoes = request.form.getlist("financeiro_opcoes")

        # Calcula pontuação (cada pergunta = 20%, cada opção = 5%)
        pontuacao = 0
        detalhes = []

        # 1. Análise de Mercado
        if concorrencia == "sim":
            pontos = len(conc_opcoes) * 5
            pontuacao += pontos
            if pontos == 20:
                detalhes.append("✅ <b>Análise de concorrência completa (20%)</b><br>• Todos os pontos mapeados.")
            elif pontos > 0:
                detalhes.append(f"⚠️ <b>Análise parcial da concorrência ({pontos}%)</b><br>• Avanço importante, mas ainda há espaço.")
            else:
                detalhes.append("🔴 <b>Falta análise de concorrência (0%)</b><br>• Risco alto. Pesquise concorrentes.")
        else:
            detalhes.append("🔴 <b>Sem análise de concorrência (0%)</b><br>• Impossível posicionar-se sem entender o mercado.")

        # 2. Conhecimento do Cliente
        if clientes == "sim":
            pontos = len(clientes_opcoes) * 5
            pontuacao += pontos
            if pontos == 20:
                detalhes.append("✅ <b>Público-alvo perfeitamente definido (20%)</b><br>• Perfil, necessidades e personas validadas.")
            elif pontos > 0:
                detalhes.append(f"⚠️ <b>Perfil do cliente parcial ({pontos}%)</b><br>• Falta entender melhor comportamento.")
            else:
                detalhes.append("🔴 <b>Conhecimento limitado do cliente (0%)</b><br>• Marketing ficará genérico.")
        else:
            detalhes.append("🔴 <b>Ausência de definição de público (0%)</b><br>• Priorize isso antes de seguir.")

        # 3. Estratégia de Marketing
        if marketing == "sim":
            pontos = len(marketing_opcoes) * 5
            pontuacao += pontos
            if pontos == 20:
                detalhes.append("✅ <b>Estratégia de marketing completa (20%)</b><br>• Posicionamento, canais e métricas definidos.")
            elif pontos > 0:
                detalhes.append(f"⚠️ <b>Estratégia em desenvolvimento ({pontos}%)</b><br>• Falta alinhar canais e medir resultados.")
            else:
                detalhes.append("🔴 <b>Sem estratégia de marketing (0%)</b><br>• Difícil atrair clientes sem plano.")
        else:
            detalhes.append("🔴 <b>Sem estratégia de marketing (0%)</b><br>• Alto risco de baixa visibilidade.")

        # 4. Estrutura e Operação
        if estrutura == "sim":
            pontos = len(estrutura_opcoes) * 5
            pontuacao += pontos
            if pontos == 20:
                detalhes.append("✅ <b>Estrutura operacional sólida (20%)</b><br>• Local, equipe, tecnologia e processos definidos.")
            elif pontos > 0:
                detalhes.append(f"⚠️ <b>Estrutura incompleta ({pontos}%)</b><br>• Falta recursos ou processos para operar.")
            else:
                detalhes.append("🔴 <b>Estrutura ausente (0%)</b><br>• Impossível operar sem planejamento.")
        else:
            detalhes.append("🔴 <b>Estrutura não definida (0%)</b><br>• Risco operacional alto.")

        # 5. Planejamento Financeiro
        if financeiro == "sim":
            pontos = len(financeiro_opcoes) * 5
            pontuacao += pontos
            if pontos == 20:
                detalhes.append("✅ <b>Plano financeiro completo (20%)</b><br>• Faturamento, fluxo de caixa e ROI projetados.")
            elif pontos > 0:
                detalhes.append(f"⚠️ <b>Controle financeiro parcial ({pontos}%)</b><br>• Falta previsão de custos ou retorno.")
            else:
                detalhes.append("🔴 <b>Falta plano financeiro (0%)</b><br>• Perigo iminente. Calcule ponto de equilíbrio.")
        else:
            detalhes.append("🔴 <b>Sem base financeira (0%)</b><br>• Não é possível gerenciar sem números.")

        # Diagnóstico Final
        if pontuacao >= 80:
            nivel = "Alta"
            cor = "green"
            recomendacao = "Seu negócio tem base sólida. Foque na execução e melhoria contínua."
            sugestoes = [
                "✅ Continue monitorando a concorrência e tendências.",
                "✅ Invista em fidelização e expansão de canais.",
                "💡 Considere contratar um consultor para escalar."
            ]
        elif pontuacao >= 60:
            nivel = "Média"
            cor = "orange"
            recomendacao = "Tem potencial, mas precisa corrigir falhas críticas antes de investir."
            sugestoes = [
                "📌 Procure um <strong>contador</strong> para estruturar seu negócio.",
                "📌 Faça <strong>treinamentos em gestão</strong> (SEBRAE, cursos online).",
                "📌 Busque <strong>consultoria gratuita</strong> (SEBRAE).",
                "📌 Valide seu produto com clientes reais."
            ]
        else:
            nivel = "Baixa"
            cor = "red"
            recomendacao = "Alto risco. Reavalie o modelo antes de avançar."
            sugestoes = [
                "⚠️ <strong>Pare investimentos grandes</strong> por enquanto.",
                "⚠️ <strong>Procure um contador</strong> urgente.",
                "⚠️ Faça um <strong>curso rápido de gestão</strong>.",
                "⚠️ Busque <strong>apoio de mentores</strong>.",
                "⚠️ Reavalie seu plano com pesquisa real."
            ]

        # Gera o gráfico
        grafico_url = gerar_grafico(pontuacao)

        return render_template("resultado.html",
                               detalhes=detalhes,
                               pontuacao=pontuacao,
                               nivel=nivel,
                               cor=cor,
                               recomendacao=recomendacao,
                               sugestoes=sugestoes,
                               grafico_url=grafico_url)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)