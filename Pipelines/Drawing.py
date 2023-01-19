

def create_image_with_values(df):

    from PIL import Image, ImageDraw, ImageFont

    values = df['aqi'].tolist()
    dt = df['datetime']

    # Define the size of the image
    width = 1400
    height = int(width/7)

    # Create a new image with a transparent background
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Define the font to use for the text
    font = ImageFont.truetype("arial.ttf", 30)

    # Draw the squares and add text to each square
    for i in range(7):
        x1 = i * (width/7)
        y1 = 0
        x2 = x1 + (width/7)
        y2 = y1 + height
        if values[i] < 50:
            square_color = (0, 255, 0)
        elif values[i] < 100:
            square_color = (255, 255, 0)
        else:
            square_color = (255, 0, 0)
        draw.rectangle([(x1, y1), (x2, y2)], fill=square_color)

        
        string = list(dt[i])
        #text_width, text_height = draw.textsize(str + f "\nAQI {values[i]}", font=font)
        #draw.text((x1+(width/7-text_width)/2, y1+(height-text_height)/2), str + f"\nAQI {values[i]}", font=font, fill=(255, 255, 255))

        #text_width, text_height = draw.textsize(f"Square {i + 1} \nValue: {values[i]}", font=font)
        #draw.text((x1+(width/7-text_width)/2, y1+(height-text_height)/2), f"Square {i + 1} \nValue: {values[i]}", font=font, fill=(255, 255, 255))

        text_width, text_height = draw.textsize(f"{string[i]} \nAQI: {values[i]}", font=font)
        draw.text((x1+(width/7-text_width)/2, y1+(height-text_height)/2), f"{string[i]} \nAQI: {values[i]}", font=font, fill=(255, 255, 255))

    # Save the image
    image.save("AQI.png", format='PNG')
    #return image

#values = [25, 75, 150, 50, 25, 100, 75]
#create_image_with_values(values)