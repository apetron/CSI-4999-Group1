const { Events, SharedEvents } = require("discord.js");

module.exports = {
    name: SharedEvents.Message,
    once: true,
    execute(client) {
        console.log(`Ready! Logged in as ${client.user.tag}`);
    },
};
