# Lab 0: onboarding with Copilot (8 minutes, no pull request)

**Story:** [DN-1](backlog/DN-1.md). **Driver:** both, each on their own machine.

## Goal

Discover the repository through Copilot, and feel the difference between asking and delegating.

## Steps

1. Open the Chat view and pick **Ask** mode. Ask:

   ```text
   Explain this repository's data flow in five bullet points, and tell me how I validate a change.
   ```

   Note which files the answer is based on (the references listed under the response).

2. Switch to **Agent** mode, in a **new chat**. Ask:

   ```text
   Run the project's preflight check and tell me whether my machine is ready.
   ```

   Approve each command manually. Before each approval, read the command.

3. Hover over the context window indicator in the chat input. Note the percentage used and the cost of the session so far.

## You are done when

- `PREFLIGHT OK` is printed (it was already green at D-1, so this should take seconds).
- You can say which command the agent chose, and whether it guessed or found it.

## What to notice

- In Ask mode, Copilot reads and answers; in Agent mode it acts through tools, and each action needs your approval.
- Without project instructions, the agent has to discover the commands. Lab 1 gives it that context.

## Fallback

Run the [manual steps](00-prerequisites.md#manual-fallback) yourself, or pair on your partner's machine.
