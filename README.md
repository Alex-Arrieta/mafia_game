# AI Mafia
We playing mafia

## Overview
The purpose of this project is to explore how large language models (LLMs), such as ChatGPT, can be integrated into the multiplayer game, Mafia, to simulate and enhance player strategies and communication. We aim to investigate how these models can build and manage knowledge graphs for each player, adapting to changing game states and potentially improving the strategic depth of gameplay. By treating each session of the language model as a distinct player, this project seeks to analyze how effectively these models can bluff, infer information, and transfer knowledge among different players.

The main goal is to understand the efficiency and limitations of LLMs in replicating or surpassing human-like strategic thinking and communication within the boundaries of a game environment. This could reveal new insights into how AI can be used to model complex social interactions and decision-making processes in a structured format. 

The context for this project involves enhancing the traditional experience of the game Mafia by incorporating advanced AI models. These models can simulate diverse player strategies, making the game more challenging and layered as they exhibit human-like behavior and reactions. This can add value to both online and offline versions of the game, creating unique scenarios where players navigate ever-evolving interactions and strategies. The application of LLMs allows for the possibility of a purely AI-driven game where human players may or may not be present, providing an always-available platform for interaction and study.

Intended users of this project include individuals or groups consisting of 0 to 4 human players who wish to include 1 to 5 non-human AI players in their games to augment the Mafia experience. This can provide flexibility in gameplay configurations and ensure full participation even when player numbers fluctuate. Additionally, developers who create or enhance Mafia bots are also viewed as primary users, as they can use these AI-driven insights to build more sophisticated, versatile game agents.


## Clone the Repository

To get a local copy of the repository, run the following command in your terminal:

```bash
git clone https://github.com/Alex-Arrieta/mafia_game.git
```

## Running the Game
To run the game, follow these steps:

1. Navigate into the project directory:

```bash
cd mafia_game
```
2. Run the game:
```bash
python3 -m main
```
This will start the game in your terminal. 

## Contributing to the Project
If you'd like to contribute, please follow the guidelines below.

1. Fork and Clone the Repository

Fork the repository on GitHub to your own account.
Clone your forked repository to your local machine using the following command:

```bash
git clone https://github.com/<your-username>/mafia_game.git
```

2. Create a New Branch

Before making any changes, create a new branch for your feature or bugfix. This helps to keep the main branch clean and makes it easier to collaborate with others.
To create and switch to a new branch:

```bash
git checkout -b feature/your-feature-name
```

Make sure to name your branch in a descriptive way (e.g., feature/add-game-sounds or bugfix/fix-typo).

3. Make Changes

Now, you can make the changes you want to contribute to the project. Remember to test your changes locally before committing.

5. Stage and Commit Your Changes

Once you’ve made your changes, add them to the staging area and commit them. Use the following commands:
Stage all changed files:

```bash
git add .
```

Commit your changes with a descriptive commit message. Follow this format:

Start with a short imperative summary (e.g., “Add new game feature”).
Include a detailed explanation of what you changed, why you changed it, and any additional context (if necessary).
Example:

```bash
git commit -m "Add new player roles to the game"
```

Commit message etiquette:

Use present tense (e.g., "Fix bug" instead of "Fixed bug").
Keep your messages short and concise. If necessary, provide more details in the body of the message.
If your commit is part of a larger feature, reference it with a prefix like feature/ or bugfix/.

5. Push Your Changes
Once your changes are committed, you need to push them to your remote repository on GitHub:

```bash
git push origin feature/your-feature-name
```

6. Create a Pull Request
After pushing your changes to GitHub, go to your repository page, and you will see an option to Create a Pull Request.

Make sure the pull request is directed towards the main branch of the original repository.
Provide a description of what you changed and why.

7. Review and Merge
Once your pull request is reviewed and approved, it will be merged into the main branch of the project.

8. Keep Your Branch Up to Date
If there are new changes to the main branch while you're working on your branch, make sure to pull the latest changes into your branch regularly to avoid conflicts.

To fetch and merge the latest changes from main into your branch:

```bash
git checkout main
git pull origin main
git checkout feature/your-feature-name
git merge main
```

Resolve any conflicts if necessary, then push your updated branch again:

```bash
git push origin feature/your-feature-name
```

Additional Notes
Branch Etiquette: Always create a new branch for each new feature or bugfix you work on. This keeps the main branch clean and allows you to work on multiple things simultaneously.
Commit Etiquette: Each commit should represent a single logical change to the project. Avoid committing multiple unrelated changes in a single commit.
Pull Requests: Provide a clear description in the pull request about the changes you made, why you made them, and how they improve the project.
KG Visualiztion: Use https://ontopea.com/ with .TTL files to visualize the KG
