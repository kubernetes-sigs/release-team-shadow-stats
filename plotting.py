# This file contains logic to generate diagrams
import matplotlib.pyplot as plt

# generic method to display percentage and amount on charts
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

# CHARTS

# chart to highlight applicant pronouns
def pronouns_chart(data):
    fig4, ax4 = plt.subplots()
    applicant_pronouns = {"he/they":0, "he/him":0, "she/her": 0, "she/they": 0, "they/them":0, "ze": 0, "neopronouns": 0, "invalid pronoun": 0}
    for e in data:
        clean_e = str(e).replace("https://www.mypronouns.org/", "", 1).lower()
        if "she" in clean_e or "her" in clean_e:
            if "they" in clean_e or "them" in clean_e:
                applicant_pronouns["she/they"] += 1
            else:
                applicant_pronouns["she/her"] += 1
        elif "him" in clean_e or "he" in clean_e:
            if "they" in clean_e or "them" in clean_e:
                applicant_pronouns["he/they"] += 1
            else:
                applicant_pronouns["he/him"] += 1
        elif "they" in clean_e or "them" in clean_e:
            applicant_pronouns["they/them"] += 1
        elif "ze" in clean_e:
            applicant_pronouns["ze"] += 1
        elif "neopronouns" in clean_e:
            applicant_pronouns["neopronouns"] += 1
        else:
            applicant_pronouns["invalid pronoun"] += 1
    # delete all pronous that do not occur
    resize_applicant_pronouns = applicant_pronouns.copy()
    for k in applicant_pronouns:
        if applicant_pronouns[k] == 0:
            del resize_applicant_pronouns[k]
    ax4.pie(resize_applicant_pronouns.values(), labels=resize_applicant_pronouns.keys(), autopct=make_autopct(resize_applicant_pronouns.values()))
    ax4.axis('equal')
    plt.show()