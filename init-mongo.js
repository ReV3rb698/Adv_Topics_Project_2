const { MongoClient } = require("mongodb");

async function initDB() {
    const client = new MongoClient("mongodb://mongo:27017");

    try {
        await client.connect();
        const db = client.db("gpa_analytics_db");

        // Create the collections if they don't exist
        const gpaCollection = db.collection("gpas");
        const analyticsCollection = db.collection("analytics");

        // Log that the initialization is done
        console.log("MongoDB initialized with collections: gpas, analytics");
    } catch (err) {
        console.error("Error initializing MongoDB: ", err);
    } finally {
        await client.close();
    }
}

initDB();
