# Instagram Helper

Simple GUI app that automates some tasks with your Instagram account.

![menu_image](https://i.ibb.co/D5L5HXB/screen.png)

## Features

* **Auto Follow** - lets you follow up to 60 users that have recently uploaded a photo to hashtag you have chosen (it can also like their pictures during the following).
* **Auto Unfollow** - lets you unfollow users from the previous run (after using **Auto Follow**) or accounts that you follow but they don't follow you back.
* **Auto Like** - lets you like photos on a provided hashtag.
* **Followers analytics** - shows which users were most active on your account (counts every like from a user and display 20 most active).
* **Likes on photos** - shows a graph with all your likes from photos so you can visualize your progress over time.
* **Account followers statistics** - shows a graph with your followers and accounts you follow over time.
* **Keep following list** - a list that you fill with names of accounts that you want to leave during **Auto Unfollow**.
* **Skip above function** - you can specify the minimum number of followers for the account to have to skip it during **Auto Unfollow**.  

more during development...

## Keep in mind
* During the runtime do not close the Chrome browser where the actions are made otherwise the program will crash.
* Every hour Instagram lets you perform an action (follow/unfollow) on 60 accounts. And you can follow on your account up to 7,500 people.

After that, you get a warning.
Even though the limits are for every hour it does not mean that Instagram will not flag you as a spammer
if you keep pushing those limits. If you want to use this program for growth of your account, just run it once a day. Or adjust the time of follows
to be longer so you can follow more people throughout the day without being blocked. I will warn you again - no one knows how the algorithm flags spam accounts so be careful.
## Getting Started

You need a Chrome browser with chromedriver installed. Chrome-driver is available in the repository in REQUIREMENT_SOFTWARE folder. Full guide on how to install it's available [here](https://chromedriver.chromium.org/). Note that you have to add it to your PATH or specify it in scripts/settings.py. 

### Prerequisites

Also, make sure you have installed Flask and selenium in your python environment. You can use requirements.txt file that you can find inside the cloned repository.

```
pip install -r requirements.txt
```

### Running

Get to the folder where you have cloned the repo and simply type

```
python3 instagram_helper.py
```

to run the server. Then in the new terminal type or simply click on the link (while pressing CTRL) provided in the console.

```
google-chrome-stable --app=http://127.0.0.1:5000/
```

chrome should open in a nice app form.

## Running the tests

If you are having some trouble, run the following file
```
pytest test.py
```

## Built With

* [Flask](https://github.com/pallets/flask) - The Python micro framework for building web applications
* [Selenium](https://selenium.dev/) - umbrella project for a range of tools and libraries that enable and support the automation of web browsers
* [Undraw](https://undraw.co/) - Open-source illustrations for every project you can imagine and create
* [Chart.js](https://www.chartjs.org/) - Simple yet flexible JavaScript charting for designers & developers

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Colorlib](https://colorlib.com/) - Great way to get inspired while designing a website