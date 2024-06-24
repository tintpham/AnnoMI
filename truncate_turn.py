import json

# load annomi data set
annomi_dataset_path = "valid.txt"

with open(annomi_dataset_path) as f:
    data = f.readlines()

def _norm(x):
    return ' '.join(x.strip().split())

turn = 10 # define the max number of turns that needs to be there. 
inputs = []
for idx, item in enumerate(data):
    line = json.loads(item)
    dialog = line['dialog']
    context = []
    for i in range(len(dialog)):
        text = _norm(dialog[i]['text'])
        
        if i > 0 and dialog[i]['speaker'] == 'sys':
                
            client_talk_type = ""
            if dialog[i-1]['speaker'] != 'sys':
                client_talk_type = dialog[i-1]['client_talk_type']
            else:
                try:
                    client_talk_type = dialog[i-2]['client_talk_type']
                except:
                    continue
            try:
                if i >= 10:
                    added_context = context[-10:]
                else:
                    added_context = context
                res = {
                    'context': " ".join(added_context.copy()),
                    'response': text,
                    'therapist_behavior': dialog[i]['strategy'],
                    'client_talk_type': client_talk_type
                }
                inputs.append(res)
            except:
                print(idx)

        context = context + [text]

with open("valid-10turn.json", "w") as f:
    json.dump(inputs, f)