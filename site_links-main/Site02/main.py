import flet as ft
import time

def main(page: ft.Page):
    page.title = "Gerador de Botões"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    url1_input = ft.TextField(label="URL do Anúncio", width=400)
    url2_input = ft.TextField(label="URL do Destino", width=400)
    result_url = ft.Text(value="", color="blue", selectable=True)

    def generate_url(e):
        if url1_input.value and url2_input.value:
            result_url.value = "Clique no link gerado abaixo para testar!"
            result_url.update()

            # Função para carregar a nova tela
            def load_button_screen(e):
                # Função para ativar o botão final
                def activate_final_button(e):
                    final_button.disabled = False
                    final_button.update()

                # Função do botão de anúncio
                def open_advertisement(e):
                    page.launch_url(url1_input.value)
                    time.sleep(3)  # Espera de 3 segundos
                    activate_final_button(e)

                # Tela de botões
                final_button = ft.ElevatedButton(
                    "Ir para o destino",
                    disabled=True,
                    on_click=lambda _: page.launch_url(url2_input.value),
                )

                advertisement_button = ft.ElevatedButton(
                    "Clique para abrir o anúncio",
                    on_click=open_advertisement,
                )

                page.clean()
                page.add(
                    ft.Text("Clique no anúncio primeiro para desbloquear o destino:"),
                    advertisement_button,
                    final_button,
                )

            page.clean()
            load_button_screen(e)

    generate_button = ft.ElevatedButton(
        "Gerar URL",
        on_click=generate_url,
    )

    # Tela inicial
    page.add(
        ft.Text("Insira as URLs para criar os botões:", size=20),
        url1_input,
        url2_input,
        generate_button,
        result_url,
    )


# Executar a aplicação Flet
ft.app(target=main)
