import io
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from django.http import HttpResponse


def create_shopping_cart(ingredients_cart):
    response = HttpResponse(content_type='application/pdf')
    response[
        'Content-Disposition'] = "attachment; filename='shopping_cart.pdf'"
    pdfmetrics.registerFont(TTFont('Arial', 'data/arial.ttf', 'UTF-8'))
    buffer = io.BytesIO()
    pdf_file = canvas.Canvas(buffer)
    pdf_file.setFont('Arial', 24)
    pdf_file.drawString(200, 800, 'Мой список покупок.')
    pdf_file.setFont('Arial', 13)

    column_x_positions = [50, 200, 350]

    from_bottom = 750
    for number, ingredient in enumerate(ingredients_cart, start=1):
        ingredient_name = ingredient['ingredient__name']
        ingredient_value = ingredient['ingredient_amount']
        unit = ingredient['ingredient__measurement_unit']

        pdf_file.drawString(
            column_x_positions[0], from_bottom, f'{number}.')
        pdf_file.drawString(
            column_x_positions[1], from_bottom, ingredient_name)
        pdf_file.drawString(
            column_x_positions[2], from_bottom, f'{ingredient_value} {unit}')

        from_bottom -= 20
        if from_bottom <= 50:
            from_bottom = 800
            pdf_file.showPage()
            pdf_file.setFont('Arial', 13)

    pdf_file.showPage()
    pdf_file.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
