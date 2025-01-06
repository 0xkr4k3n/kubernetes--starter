// server.js
const express = require('express');
const mysql = require('mysql2/promise');

const app = express();
const PORT = 3000; // or any port you prefer

// 1. Create a MySQL connection pool (recommended for production)
const pool = mysql.createPool({
  host: 'url-db',              // Docker Compose service name, if running in Docker
  user: 'urluser',         // match the user in your MySQL environment
  password: 'urlpass',     // match the password in your MySQL environment
  database: 'url_db',      // the database name
  port: 3306               // internal MySQL port
});

// 2. Define a route for short URLs
app.get('/:shortUrl', async (req, res) => {
  const { shortUrl } = req.params;

  try {
    // Query the URL table to find the matching entry
    const [rows] = await pool.execute(
      'SELECT long_url FROM url WHERE short_url = ? LIMIT 1',
      [shortUrl]
    );
    
    if (rows.length === 0) {
      // No record found -> send a 404 or custom response
      return res.status(404).json({ error: 'Short URL not found' });
    }

    // If found, redirect to the long URL
    const longUrl = rows[0].long_url;
    res.redirect(longUrl);

  } catch (err) {
    console.error('Error querying database:', err);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// 3. Start the server
app.listen(PORT, () => {
  console.log(`Express server listening on port ${PORT}`);
});
