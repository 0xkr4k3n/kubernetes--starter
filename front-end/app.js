document.getElementById('urlForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const longUrl = document.getElementById('urlInput').value;
    try {
      const response = await fetch('http://127.0.0.1:5000/shorten', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ longUrl })
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log(data.shortUrl)
        document.getElementById('result').innerText = `Shortened URL: ${data.shortUrl}`;
      } else {
        alert('Failed to shorten the URL!');
      }
    } catch (error) {
      alert('Error: ' + error.message);
    }
  });
  