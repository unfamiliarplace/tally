from pathlib import Path
from datetime import date
import csv

ANON = '--'

names = {} # TODO unused
choices = {}

print()
print("=====")
print('TALLY')
print("=====")
print()

print('Enter choices one by one. Blank to quit')
print('Lines with : will be interpreted as name : choice')
print()

choice = input('Next: ').strip().lower()
while choice != '':
    if ':' in choice:
        name, choice = (s.strip() for s in choice.split(':'))
    else:
        name = ANON
    
    names[name] = names.get(name, []) + [choice]
    choices[choice] = choices.get(choice, []) + [name]

    choice = input('Next: ').strip().lower()

print()
print('=======')
print('Results')
print('=======')
print()

longest_choice = len(max(choices, key=len))
longest_tally = len(str(len(max(choices.values(), key=len))))

def order_choices() -> list[str]:
    return sorted(choices, key=lambda c: (len(choices[c]), tuple(-ord(m) for m in c.lower())), reverse=True)

def order_real_names(subnames: list[str]) -> list[str]:
    return sorted(list(filter(lambda c: c != ANON, subnames)))

for choice in order_choices():
    choosers = choices[choice]
    non_anon = order_real_names(choosers)
    print(f'{choice.ljust(longest_choice)} : {str(len(choosers)).rjust(longest_tally)}', end='')
    if non_anon:
        print(f' > {", ".join(non_anon)}', end='')
    n_anon = len(choosers) - len(non_anon)
    if non_anon and n_anon:
        print(f' ({n_anon} anonymous)', end='')
    print()

print()
save = input('Save to a file? [Y/N ; default Y]: ').strip().upper()
if (not save) or (save == 'Y'):
    tag = input('Tag: ')

    Path.mkdir(Path('./output'), parents=True, exist_ok=True)
    ts = date.today().strftime('%Y-%m-%d')
    path = Path(f'output/{ts} {tag}.csv')

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Choice', '#', 'Names'])

        for choice in order_choices():
            choosers = choices[choice]
            non_anon = order_real_names(choosers)
            n_anon = len(choosers) - len(non_anon)

            row = [choice, len(choosers), non_anon]
            if non_anon and n_anon:
                non_anon.append(f'({n_anon} anonymous)')
            writer.writerow(row)
        
        print(f'Saved to {path}')

input('Press Enter to exit')
