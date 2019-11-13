import json
import os


def str2json(context, questions):
    print(questions)
    ans = [{"answer_start": 0, "text": ""}]
    path = os.path.join(os.getcwd(), 'BiDAF')
    path = os.path.join(path, 'testing_files')

    try:
        os.remove(os.path.join(path, 'test1.jsonl'))
        os.remove(os.path.join(path, 'test1.json'))
    except FileNotFoundError:
        pass

    # if os.path.exists(os.path.join(path, 'test1.json')):
    #     with open(os.path.join(path, 'test1.json'), 'r') as json_file:
    #         data = json.load(json_file)
    # else:
    data = {'data': []}
    data['data'].append({
        'title': 'Q&A',
        'paragraphs': [{'context': context, 'qas': [{'answers': ans, 'question': '', 'id': ''}]}]
    })

    id = 0x0
    index = 0
    for question in questions:
        try:
            data['data'][0]['paragraphs'][0]['qas'][index]['question'] = question
            data['data'][0]['paragraphs'][0]['qas'][index]['id'] = id
            for _ in range(2):
                data['data'][0]['paragraphs'][0]['qas'].append({'answers': ans, 'question': question, 'id': id})
            index = 0x40000

        except IndexError:
            for _ in range(3):
                data['data'][0]['paragraphs'][0]['qas'].append({'answers': ans, 'question': question, 'id': id})
        id += 1

    with open(os.path.join(path, 'test1.json'), 'w+') as outfile:
        json.dump(data, outfile)
