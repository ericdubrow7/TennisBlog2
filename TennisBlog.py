from flask import Flask, render_template

app = Flask(__name__)

# Sample blog posts
posts = [
    {
        'title': 'Latest news on military movements in Iran',
        'author': 'John Doe',
        'date': 'October 3, 2024',
        'content': 'Iran launched almost 200 ballistic missiles towards Israel on Tuesday night. The Israeli military said most of the missiles were intercepted, but that a small number struck central and southern Israel. The only person reported to have been killed was a Palestinian man in the occupied West Bank. It was Iran’s second such attack on Israel this year, after it launched about 300 missiles and drones in April. Heres what we know so far.'
    },
    {
        'title': 'US Open 2024: Exciting Quarterfinal Matches',
        'author': 'John Doe',
        'date': 'September 15, 2024',
        'content': 'The US Open quarterfinals are packed with thrilling matches...'
    },
    {
        'title': 'Wimbledon 2024: Djokovic Eyes Another Title',
        'author': 'Jane Smith',
        'date': 'July 10, 2024',
        'content': 'Novak Djokovic is ready to defend his Wimbledon crown...'
    },
    {
        'title': 'US Open 2023: Carlos Alcaraz Defends His Title in Thrilling Five-Set Final',
        'author': 'Eric Dubrow',
        'date': 'September 15, 2024',
        'content': "The 2024 US Open concluded with an exhilarating final as Spain’s Carlos Alcaraz successfully defended his title in an epic five-set match against Norway’s Casper Ruud. Alcaraz, who has been a rising star in tennis over the last few years, showcased his resilience and fighting spirit to secure his second consecutive US Open trophy. In front of a packed Arthur Ashe Stadium, Alcaraz triumphed 6-4, 3-6, 7-6 (7-5), 2-6, 6-3, solidifying his position as one of the top contenders in the sport. This victory brings his Grand Slam tally to three, further solidifying his status as a future legend in men’s tennis."   
    },
    {
        'title': 'US Open 2023: Carlos Alcaraz Defends His Title in Thrilling Five-Set Final',
        'author': 'Eric Dubrow',
        'date': 'September 15, 2024',
        'content': "The 2024 US Open concluded with an exhilarating final as Spain’s Carlos Alcaraz successfully defended his title in an epic five-set match against Norway’s Casper Ruud. Alcaraz, who has been a rising star in tennis over the last few years, showcased his resilience and fighting spirit to secure his second consecutive US Open trophy. In front of a packed Arthur Ashe Stadium, Alcaraz triumphed 6-4, 3-6, 7-6 (7-5), 2-6, 6-3, solidifying his position as one of the top contenders in the sport. This victory brings his Grand Slam tally to three, further solidifying his status as a future legend in men’s tennis."   
    },
    {
        'title': 'US Open 2023: Carlos Alcaraz Defends His Title in Thrilling Five-Set Final',
        'author': 'Eric Dubrow',
        'date': 'September 15, 2024',
        'content': "### Recent Highlights from the ATP Tour\n\nAs the ATP Tour continues to unfold its 2023 season, fans have witnessed some thrilling matches and unexpected developments that have shaped the landscape of men’s tennis. From emerging talents to seasoned veterans making their mark, the tournament cycles have provided excitement and drama in equal measure.\n\n#### Rise of the New Generation\n\nOne of the standout stories of the recent weeks has been the emergence of young players who are making their presence felt in the top tiers of the ATP rankings. Players like Jannik Sinner and Carlos Alcaraz have not only challenged the established order but have also captured titles at prestigious events, including the Masters 1000 tournaments. Their dynamic playing styles and mental toughness are drawing comparisons to the legendary Big Three, and the tennis world is abuzz with speculation about the future rivalries.\n\n#### Djokovic's Continued Dominance\n\nNovak Djokovic, the current ATP World No. 1, continues to demonstrate his dominance on the tour. After a stellar performance at Wimbledon, where he secured his 24th Grand Slam title, Djokovic added another trophy to his collection with a commanding victory at the Cincinnati Masters. His unmatched consistency and ability to perform under pressure have cemented his status as one of the sport's greats, leaving fans to ponder how many more records he can break.\n\n#### Injury Concerns and Comebacks\n\nInjuries have played a significant role in the 2023 season, with several top players, including Rafael Nadal, having to navigate time away from the court. Nadal's absence has opened up opportunities for other competitors to gain traction in the rankings, but the tennis community remains hopeful for his return. On the flip side, players like Andy Murray have shown resilience, making headlines with remarkable performances, highlighting the spirit of competition and the excitement of comebacks.\n\n#### The Race to the ATP Finals\n\nAs the season progresses, the race towards the prestigious ATP Finals is heating up. Players are vying for a coveted spot, and with only a few months left to qualify, the stakes are higher than ever. The ongoing battle within the top 10 has fans anticipating intense showdowns, especially at the upcoming US Open, where players will look to solidify their standings and gain crucial points.\n\n#### Conclusion\n\nThe ATP Tour continues to captivate audiences this season, with a blend of young talent and legendary prowess. As the world's best prepare for the last Grand Slam of the year, fans can expect nothing short of thrilling encounters and historical moments. With the future of men's tennis looking bright, the excitement is palpable as players strive to leave their mark on the sport's rich history."   
    } 
]

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = posts[post_id]
    return render_template('post.html', post=post)

@app.route('/abouttheauthor')
def abouttheauthor():
    return render_template('abouttheauthor.html')

if __name__ == '__main__':
    app.run(debug=True)
