#imports for data analysis/visualization
from matplotlib.pyplot import*
import csv
#import pandas

prompts = []
responses = []

# Read data from the CSV file
with open('prompt_history.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row if there is one
    for row in reader:
        prompts.append(row[0])      # Add the first column (Prompts) to the prompts list
        responses.append(row[1])    # Add the second column (Responses) to the responses list

personal_pronouns = [
    " i ", " ii ", " I ", " II ",  # I
    " yuo ", " yiu ", " You ", " YOU ", " Yuo ", " YOu ", " you ",  # you
    " hee ", " He ", " HE ", " HEE ", " he ",  # he
    " She ", " SHE ", " SHEE ", " she ",  # she
    " itt ", " It ", " IT ", " Itt ", " ITT ", " it ",  # it
    " We ", " WE ", " we ",  # we
    " teyh ", " thye ", " they ", " THEY ", " They ", " THEY ", " Teyh ",  # they
    " tehm ", " thme ", " them ", " THEM ", " Them ", " THEM ", " Tehm ",  # them
    " su ", " u ", " uss ", " Us ", " US ", " Uss ", " USS ",  # us
    " mih ", " hiim ", " hmi ", " im ", " hm ", " Him ", " HIM ", " Mih ",  # him
    " reh ", " heer ", " ehr ", " hr ", " hee ", " Her ", " HER ", " Reh ",  # her
    " ihs ", " hsi ", " hiss ", " hi ", " hs ", " His ", " HIS ", " Ihs ",  # his
    " hees ", " hrse ", " herss ", " hres ", " ers ", " Hers ", " HERS ", " Hees ",  # hers
    " tsi ", " itts ", " ist ", " itz ", " Its ", " ITS ", " Itt ", " ITZ ",  # its
    " thiers ", " theirss ", " their ", " thirs ", " teirs ", " Theirs ", " THEIRS ", " Thiers ",  # theirs
    " oru ", " ourr ", " ou ", " Our ", " OUR ", " Oru ", " OURR ",  # our
    " yoru ", " yuor ", " yourr ", " yor ", " Your ", " YOUR ", " Yoru ", " YOURR ",  # your
    # Contractions and their common errors
    " I'm ", " i'm ", " im ", " I'M ",  # I'm
    " he's ", " He's ", " heS ", " hes ", " HE's ",  # he's
    " she's ", " She's ", " sheS ", " shes ", " SHE's ",  # she's
    " it's ", " It's ", " itS ", " its ", " IT's ",  # it's
    " we're ", " We're ", " weRe ", " wer ", " WE're ",  # we're
    " they're ", " They're ", " theyRe ", " thayre ", " THEY'RE ",  # they're
    " I'mma ", " Imma ", " ImMA ", " i'mma ", " imma ",  # I'mma
    " can't ", " Cant ", " can'tt ", " CAnt ", " CANT ",  # can't
    " don't ", " dont ", " Don’t ", " DON'T ", " dn't ",  # don't
    " won't ", " Wont ", " wonnt ", " WON'T ", " wnt ",  # won't
    " you'll ", " youll ", " Youll ", " YOU'LL ", " youll ",  # you'll
    " he'll ", " hell ", " HE'LL ", " he’ll ",  # he'll
    " she'll ", " shes ", " SHE'LL ", " she’ll ",  # she'll
    " they'll ", " theyll ", " THEY'LL ", " they’ll ",  # they'll
    " I'd ", " i'd ", " I'D ", " Id ",  # I'd
    " you'd ", " you'd ", " YOU'D ", " youd ",  # you'd
    " he'd ", " he'd ", " HE'D ", " hed ",  # he'd
    " she'd ", " she'd ", " SHE'D ", " shed ",  # she'd
    " they'd ", " they'd ", " THEY'D ", " theyd ",  # they'd
    # Possessive pronouns and their errors
    " his ", " his ", " HIS ", " hiss ", " HISs ",  # his
    " hers ", " Hers ", " HERS ", " hirs ", " HERs ", " Herss ", " herS ",  # hers
    " its ", " Its ", " ITS ", " its ", " ITs ", " itS ",  # its
    " their ", " Theirs ", " THEIRS ", " thier ", " thierS ",  # theirs
    " my ", " My ", " MY ", " mi ", " MYy ", " myy ",  # my
    " your ", " Your ", " YOUR ", " youre ", " YOURs ", " yr ", " yur ", " yoour ",  # your
]


conv_num = len(prompts)
ppcount = 0
for prompt in prompts:
    for personal_pronoun in personal_pronouns:
        if personal_pronoun in prompt:
            ppcount += 1
            break

barh(0, ppcount, color='blue', label='Prompts with Pronouns')
barh(0, conv_num-ppcount, color='orange', left=ppcount, label='Impersonal Prompts')
xlabel('Count')
title('Pronoun Usage in Prompts')
legend()
gca().get_yaxis().set_visible(False)
xticks(range(0, conv_num+1))
show()