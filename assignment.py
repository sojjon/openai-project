import openai
import os
import base64
import requests
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('openai_api')
api_endpoints = os.getenv('endpoints')
pixabay_api = os.getenv('pixabay_key')
wp_user = os.getenv('user')
wp_password = os.getenv('password')
wp_credential = f'{wp_user}:{wp_password}'
wp_token = base64.b64encode(wp_credential.encode())
wp_headers = {'Authorization':f'Basic {wp_token.decode("utf-8")}'}


file = open('keywords.txt','r')
kw = file.readlines()
file.close()
for keyword in kw:
    intro = f'write a 80 words introduction about {keyword}'
    importance = f'writhe 100 words about the importance of {keyword}'
    choosing_product = f'write 100 words about what to know before buy {keyword}'
    conclusion = f'write 50 words conclusion about {keyword}'

    #image
    KEY = pixabay_api
    query = keyword
    while ' ' in query:
        query = query.replace(' ', '+')
    url = f'https://pixabay.com/api/?key={KEY}&q={query}&image_type=photo'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        images = data.get('hits')
        for image in images:
            picture = image.get('webformatURL')


    def media_from_url(img_src, alter_text):
        codes = f'<!-- wp:image {{"align":"center","sizeSlug":"large"}} --> ' \
                f'<figure class="wp-block-image aligncenter size-large">' \
                f'<img src="{img_src}" alt="{alter_text}"/>' \
                f'<figcaption class="wp-element-caption">{alter_text}</figcaption></figure>' \
                f'<!-- /wp:image -->'
        return codes


    def openai_answer(my_prompt):
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=my_prompt,
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        data = response.get('choices')[0].get('text').strip('\n')
        return data



    def wp_paragraph(text):
        paragraph = f'<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->'
        return paragraph


    def wp_heading_two(text):
        heading_two = f'<!-- wp:heading --><h2> {text}</h2><!-- /wp:heading -->'
        return heading_two


    intro_para = wp_paragraph(openai_answer(intro))
    wp_picture = media_from_url(picture, query)
    importance_heading = wp_heading_two(f'Why Do You Need a {keyword}')
    importance_para = wp_paragraph(openai_answer(importance))
    choosing_product_heading = wp_heading_two(f'Know This Before Buy a {keyword} ')
    choosing_product_para = wp_paragraph(openai_answer(choosing_product))
    conclusion_heading = wp_heading_two(f'Conclusion')
    conclusion_para = wp_paragraph(openai_answer(conclusion))


    content = intro_para+wp_picture+importance_heading+importance_para+choosing_product_heading+choosing_product_para+conclusion_heading+conclusion_para


    title = f'The Best {keyword} in 2022'
    title = title.title()


    data = {
        'title': title,
        'content': content,
    }

    res = requests.post(api_endpoints, data=data, headers=wp_headers)
