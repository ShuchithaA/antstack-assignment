import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_KEY = 'AIzaSyDHbKuBnSTA-2BwdqHEm5WcXad5AyQaTaA';
const API_URL = `https://tenor.googleapis.com/v2/search?q='friends'&key=${API_KEY}&limit=10`;

function TenorGifApp() {
  const [gifs, setGifs] = useState([]);

  useEffect(() => {
    axios.get(API_URL)
      .then((response) => {
        setGifs(response.data.results);
      })
      .catch((error) => {
        console.error('Error fetching GIFs from Tenor:', error);
      });
  }, []);

  return (
    <div>
      <h1>Tenor GIFs</h1>
      <div className="gif-container">
        {gifs.length > 0 ? (
          gifs.map((gif) => (
            <img
              key={gif.id}
              src={gif.media_formats?.nanowebp_transparent?.url || ''}
              alt={gif.title}
            />
          ))
        ) : (
          <p>No GIFs found</p>
        )}
      </div>
    </div>
  );
}

export default TenorGifApp;


