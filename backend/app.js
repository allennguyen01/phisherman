import OpenAI from 'openai';
import express from 'express';
import dotenv from 'dotenv';
import axios from 'axios';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

const openai = new OpenAI({ apiKey: process.env.OPEN_AI_API_KEY });

// Endpoint to receive parameters and return diet plan
app.post('/phisherman-response', async (req, res) => {
	const { spamScore, discordMessage } = req.body;

	try {
		const phishermanRes = await generatePhishermanResponse(
			spamScore,
			discordMessage,
		);
		res.send(phishermanRes);
	} catch (error) {
		console.error(error);
		res.status(500).send(error.message);
	}
});

async function generatePhishermanResponse(spamScore, discordMessage) {
	const prompt = `A user received the following message on Discord: "${discordMessage}" and the message was given a spam probability score of ${spamScore} (scale of 0.0 to 1.0 where 1.0 indicates that it is a spam message). Please respond with a message to the user that restates the spam probability score and explains why the message is or is not spam.`;

	const completion = await openai.chat.completions.create({
		model: 'gpt-3.5-turbo',
		messages: [
			{ role: 'system', content: 'You are a cybersecurity expert.' },
			{ role: 'user', content: prompt },
		],
	});

	console.log(completion.choices[0].message.content);
	return completion.choices[0].message.content;
}

// Start the server	
app.listen(port, () => {
	console.log(`Server is running on port ${port}`);
});
