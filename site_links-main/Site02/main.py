from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Rota principal para receber as URLs e gerar a URL personalizada
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url1 = request.form.get("url1")
        url2 = request.form.get("url2")
        if url1 and url2:
            return redirect(url_for("button_page", ad_url=url1, target_url=url2))
    return '''
    <form method="post">
        URL do anúncio: <input type="text" name="url1"><br>
        URL de destino: <input type="text" name="url2"><br>
        <input type="submit" value="Gerar URL">
    </form>
    '''

# Rota para exibir a página com os botões
@app.route("/buttons")
def button_page():
    ad_url = request.args.get("ad_url")
    target_url = request.args.get("target_url")
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Página com Botões</title>
        <script>
            let adOpened = false;

            function openAd(url) {
                window.open(url, "_blank");
                adOpened = true;
                setTimeout(() => {
                    if (adOpened) {
                        document.getElementById("targetButton").disabled = false;
                    }
                }, 3000);
            }
        </script>
    </head>
    <body>
        <h1>Escolha uma ação:</h1>
        <button onclick="openAd('{{ ad_url }}')">Abrir Anúncio</button><br><br>
        <button id="targetButton" onclick="location.href='{{ target_url }}'" disabled>Ir para o Destino</button>
    </body>
    </html>
    '''
    return render_template_string(html_template, ad_url=ad_url, target_url=target_url)

if __name__ == "__main__":
    app.run(debug=True)
