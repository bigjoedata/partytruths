# Visit [PartyTruths.com](partytruths.com) to see the site in action. 
I have omitted some code from this repository since it needs to be cleaned up but have kept some pieces I found helpful, mainly the components needed to deploy on Docker

# 📣 About PartyTruths.com
> I frequently hear claims that don't smell right. I wanted a snappy way to quickly give me the unvarnished facts. This tool isn't built to cherry-pick data points, rather it's the first part of casting a wide net.  There is a larger context to these data points and this app should just be the start of any exploration.

The user-interface is purposefully sparse. Hover over charts to see details. Click the help button if anything is unclear.

If you have any issues and/or requests submit to the [Github](https://github.com/bigjoedata/partytruths/issues).


## Notes / Things to consider:
 - The help button will reveal annotations. I have kept documentation and interface minimal and put help text where needed
 - All data is specific to the United States unless otherwise noted
 - Data is structured my own taxonomy, which I will continue to revise
 - I have been selective about both my data points and sources. There are many wells to pull from, but I have tried to err on the side of generally acceptable sources. I try to show inflation or adjusted numbers wherever appropriate.
 - The emphasis is on descriptive statistics. Statistical modeling is omitted at this time, I may add with accompanying interpretation guidance at a later date, but this app is more about breadth than depth.
 - All data is averaged by year. This decision was made for several reasons, including smoothing out seasonality and other short term fluctuations. The current year may be more volatile as a result.
 - *Lastly, my immediate to-do list includes adding better ways to understand the trajectory of 2020, including health issues, race relations and police-civilian interactions. There are numerous data sources for these, it's just a identifying the most appropriate.
  
## What were my technical goals when building this
- I created a similar tool in the past using Alteryx and Tableau but wanted to build something new.
- Control the full tech stack. Use Python / [Open Source Software] (https://en.wikipedia.org/wiki/Open-source_software) wherever possible
- Keep simple and clean with adaptive interface
- Make portable / easily deployable on cloud services, Kubernetes, Docker
- Make it easy for me to add new data sources
- Always up to date with integrated web API data pulls
- Mobile Friendly
- *Mostly* Follow [best practices](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745) including [Pep8](https://www.python.org/dev/peps/pep-0008/) and [Pep20](https://www.python.org/dev/peps/pep-0020/)

## Tech Stack
- This app is 100% powered by various [Python](https://www.python.org/) tools. Data is retrieved through various APIs upon load and cached for rapid retrieval.
- [Streamlit](https://streamlit.io/) is a Python based app framework and forms the heart of this project. It grants the ability to bring code to life by serving up programmatically controlled widgets and charts. Importantly it provides caching to minimize API calls. Additional functionality added with [Awesome Streamlit](https://github.com/MarcSkovMadsen/awesome-streamlit) library.
- [Pandas](https://pandas.pydata.org/) is the ubiquitous data analysis library for Python.
- Most charts are created in [Altair,](https://altair-viz.github.io/index.html)a powerful interactive Python visualization library based on [Vega.](https://vega.github.io/vega/) Enables custom themes and can read Pandas dataframes directly. Javascript makes it light and fast.
- [Pandas Profiling](https://github.com/pandas-profiling/pandas-profiling) using the [Streamlit Components](https://docs.streamlit.io/en/stable/streamlit_components.html) [package](https://github.com/Ghasel/streamlit-pandas-profiling/).
- [Google Sheets](https://www.google.com/sheets/about/) Helps organize my data sources easily to support the backend
- [Gspread](https://github.com/burnash/gspread) Retrieve data from Google Sheets through Python using OAuth 2.0

## Data Sources, References and Other Tools Consulted
- [Awesome Streamlit](https://github.com/MarcSkovMadsen/awesome-streamlit) A curated list of Streamlit resources with many examples
- [Quandl](https://www.quandl.com/) A data aggregator. Known for financial data but has many data sets. Provides unified API with Python wrapper
- [Streamlitopedia](https://pmbaumgartner.github.io/streamlitopedia/) Another collection of Streamlit resources. The "Custom1" and "Custom2" themes come from here.
- [StackEdit](https://stackedit.io/) In browser [Markdown](https://en.wikipedia.org/wiki/Markdown) GUI
- [Coolors](https://coolors.co/) for color palette generation. I have tried to be color blind friendly.
- [Hatchful](https://hatchful.shopify.com/) Helped me create the site logo

## TO-DO

 - [ ]   Add more data points to reflect current events
 - [ ]   Show random datapoint(s) as default
 - [ ]   As always, refactor code, optimize further 
 - [ ]   Add additional adjustments (e.g., inflation, Index Scores, logarithmic scaling) for alternate comparability
 - [ ]   Add more emojis. They make me smile
