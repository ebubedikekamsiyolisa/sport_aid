# install plotly
# pip install plotly
import plotly.express as px

df = px.data.gapminder().query("year == 2007")
#px.data.gapminder() loads a built-in sample dataset
#It contains country-level stats — population, life expectancy,
# GDP per capita — tracked every 5 years from 1952 to 2007.
fig = px.scatter(
    df, x='gdpPercap', y='lifeExp', size='pop', color='continent',
    hover_name='country', log_x=True, size_max=60,
    title='GDP per Capita vs Life Expectancy (2007)'
)
fig.show()
#df — the filtered 2007 data to plot
#x='gdpPercap' — horizontal axis = GDP per capita for each country
#y='lifeExp' — vertical axis = life expectancy for each country
#size='pop' — the size of each dot scales with that country's population (bigger population = bigger bubble)
#color='continent' — dots are color-coded by continent, so you can visually group countries (e.g., all African countries the same color)
# hover_name='country' — when you hover your mouse over a dot, it shows the country name in the tooltip
# log_x=True — plots the x-axis (GDP) on a logarithmic scale instead of linear. This matters because GDP per capita varies hugely (some countries near $500, others near $50,000) — a log scale spreads out the low values so they're not all crushed together on the left
# size_max=60 — caps the maximum bubble size in pixels, so the largest-population country (e.g., China) doesn't dominate the whole chart
# title='...' — sets the chart's title text