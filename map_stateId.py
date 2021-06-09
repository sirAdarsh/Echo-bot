import json    

with open ('state.json') as d:
    state_dict = json.loads(d.read())

s = state_dict['states']
# print(s)

# for state in s:
#     print(state['state_id'], "    ", state['state_name'])

state_id_dict = dict()

for state in s:
    state_id = state['state_id']
    state_name = state['state_name']
    state_id_dict[state_name] = state_id

for state in state_id_dict:
    print(state, "  ", state_id_dict[state])