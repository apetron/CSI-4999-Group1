const { Client, Events, GatewayIntentBits } = require("discord.js");
const { token } = require("./config.json");
const path = require("node:path");
const fs = require("node:fs");

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

const eventsPath = path.join(__dirname, "events");
console.log(eventsPath);
const eventFiles = fs.readdirSync(eventsPath).filter((file) => file.endsWith(".js"));
console.log(eventFiles);

for (const file of eventFiles) {
    const filePath = path.join(eventsPath, file);
    console.log(filePath);
    const event = require(filePath);
    if (event.once) {
        console.log("once");
        client.once(event.name, (...args) => event.execute(...args));
    } else {
        console.log("on");
        client.on(event.name, (...args) => event.execute(...args));
    }
}

client.login(token);
