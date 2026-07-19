import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import micropip
    from random import sample
    import secrets

    import marimo as mo



    return micropip, mo, sample, secrets


@app.cell
async def _(micropip):
    try:
        from wonderwords import RandomWord
    except ModuleNotFoundError:
        await micropip.install('wonderwords')
        from wonderwords import RandomWord
    return (RandomWord,)


@app.cell
def _(mo):
    word_categories = ['Verbs', 'Adjectives', 'Nouns']

    verbcounter = mo.ui.slider(start=1, stop=5, value =1, show_value= True, label='Number of Verbs: ') 
    adjectivecounter = mo.ui.slider(start=1, stop=5, value =1, show_value= True, label='Number of  Adjectives: ')
    nouncounter = mo.ui.slider(start=1, stop=5, value =1, show_value= True, label='Number of  Nouns: ')

    intlength = mo.ui.slider(start=1, stop=10, value =2, label='Number of of digits: ', show_value= True)

    randomize = mo.ui.switch(value=False, label='Randomize word and number order')
    optionscounter = mo.ui.slider(start=1, stop=50, value=10, label='Number of options to output', show_value=True)

    refreshbutton = mo.ui.button(label='Click to generate new passphrases')

    sidebar_title = mo.md('## Settings')

    mo.sidebar(
        mo.vstack([sidebar_title, verbcounter, adjectivecounter, nouncounter, intlength, randomize, optionscounter],
                 align='end'),
        width='500px',
        footer=refreshbutton,
    )
    return (
        adjectivecounter,
        intlength,
        nouncounter,
        optionscounter,
        randomize,
        refreshbutton,
        verbcounter,
        word_categories,
    )


@app.cell
def _(RandomWord, word_categories):
    # Initialize word cache

    r = RandomWord()
    wordcache = {cat: r.filter(include_parts_of_speech=[cat.lower()]) for cat in word_categories}
    return (wordcache,)


@app.cell
def _(
    adjectivecounter,
    intlength,
    nouncounter,
    randomize,
    sample,
    secrets,
    verbcounter,
    wordcache,
):
    def generate_passphrase(
        verbcount = verbcounter.value,
        adjectivecount = adjectivecounter.value,
        nouncount = nouncounter.value,
        intlength = intlength.value,
        randomize = randomize.value,  
    ):
        categories = (['Verbs']*verbcount 
            + ['Adjectives']*adjectivecount
            + ['Nouns']*nouncount)

        words = [secrets.choice(wordcache[cat]).capitalize() for cat in categories]

        words += [f'{secrets.randbelow(10**intlength):0{intlength}d}']

        if randomize:
            words = sample(words, len(words))

        return ''.join(words)

    return (generate_passphrase,)


@app.cell
def _(generate_passphrase, mo, optionscounter, refreshbutton):
    refreshbutton

    outputlist = [generate_passphrase() for _ in range(optionscounter.value)]

    mo.ui.table(
        outputlist,
        selection='single-cell',
        show_search=False,
        label='## Choose the option you like best',
        page_size=50
    )
    return


if __name__ == "__main__":
    app.run()
