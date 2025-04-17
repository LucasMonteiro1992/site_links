import flet as ft
from flet import Image, Text, Column, Container, TextField, ElevatedButton, icons, Row
import asyncio

def main(page: ft.Page):
    page.title = "Cloudwalk Payments"
    page.window_icon = "logo.png"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Arquivos locais
    logo_path = "logo.png"
    qr_code_path = "qrcode.png"

    # Informações do pagamento
    valor = "R$ 9,90"
    codigo_pix = """00020101021126580014BR.GOV.BCB.PIX01360c2884fc-0fd2-4e7d-b93b-73a95a2277ab52040000530398654049.905802BR5916Giordana Barreto6008SAOPAULO61080132305062070503***63047DE6"""

    # Cabeçalho com logo e texto
    logo_header = Row(
        controls=[
            Image(src=logo_path, width=40, height=40, fit=ft.ImageFit.CONTAIN),
            Text("Cloudwalk Payments", size=22, weight="bold"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    # Componentes visuais
    valor_texto = Text(valor, size=30, weight="bold", color="green600")
    qr_code = Image(src=qr_code_path, width=250, height=250, fit=ft.ImageFit.CONTAIN)
    nome_texto = Text("Giordana Barreto", size=16, weight="w500")

    codigo_field = TextField(
        value=codigo_pix,
        read_only=True,
        multiline=True,
        max_lines=3,
        expand=True,
        border=ft.InputBorder.OUTLINE,
    )

    # Cronômetro (inicialmente invisível)
    tempo_restante = 180
    cronometro_text = Text("Código expira em 03:00", size=14, color="red600", visible=False)

    async def atualizar_cronometro():
        nonlocal tempo_restante
        cronometro_text.visible = True
        await page.update_async()
        while tempo_restante > 0:
            await asyncio.sleep(1)
            tempo_restante -= 1
            minutos = tempo_restante // 60
            segundos = tempo_restante % 60
            cronometro_text.value = f"Código expira em {minutos:02d}:{segundos:02d}"
            await page.update_async()
        cronometro_text.value = "⚠️ Código expirado"
        cronometro_text.color = "red"
        await page.update_async()

    def copiar_codigo(e):
        page.set_clipboard(codigo_pix)
        page.snack_bar = ft.SnackBar(content=Text("✅ Código Pix copiado com sucesso!"))
        page.snack_bar.open = True
        page.update()
        page.run_task(atualizar_cronometro)

    copiar_botao = ElevatedButton(
        text="Copiar código Pix",
        icon=icons.CONTENT_COPY,
        on_click=copiar_codigo,
        style=ft.ButtonStyle(padding=20)
    )

    def vip_bloqueado(e):
        page.snack_bar = ft.SnackBar(content=Text("⚠️ Pagamento ainda não foi efetuado."))
        page.snack_bar.open = True
        page.update()

    vip_botao = ElevatedButton(
        text="Conteúdo VIP",
        icon=icons.LOCK,
        on_click=vip_bloqueado,
        style=ft.ButtonStyle(padding=20),
    )

    # Interface
    page.add(
        Column([
            Container(logo_header, alignment=ft.alignment.center),
            Container(valor_texto, alignment=ft.alignment.center),
            Container(qr_code, alignment=ft.alignment.center),
            Container(nome_texto, alignment=ft.alignment.center),  # <- Nome adicionado aqui
            Container(codigo_field, alignment=ft.alignment.center),
            Container(copiar_botao, alignment=ft.alignment.center),
            Container(vip_botao, alignment=ft.alignment.center),
            Container(cronometro_text, alignment=ft.alignment.center),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20)
    )

ft.app(target=main)
