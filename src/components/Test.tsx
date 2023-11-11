import React, { useState } from "react";
import TextField from "@mui/material/TextField";
import { Button } from "@mui/material";
import axios from "axios";
import { CircularProgress, Grid, Typography } from "@mui/material";

export default function Test() {
  const apiBaseUrl =
    "https://rm6d2u6rug4f5lt3mxwstjfmoe0jemgi.lambda-url.eu-central-1.on.aws";
  const base_url = "https://cookidoo.de";
  const [url, setUrl] = useState("");
  const [jwt, setJwt] = useState("");
  const [jsonRecipe, setJsonRecipe] = useState("\n\n\n\n\n");
  const [parsedRecipe, setParsedRecipe] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleParseWebsite = async () => {
    if (url.trim().length === 0) {
      return;
    }
    setIsLoading(true);
    try {
      const response = await axios.get(apiBaseUrl + "/?url=" + url); // Replace with your website parsing logic
      setJsonRecipe(JSON.stringify(response.data));
      setParsedRecipe(response.data);
    } catch (error) {
      console.error("Error parsing website:", error);
    }
    setIsLoading(false);
  };

  return (
    <>
      <TextField
        fullWidth
        id="txtUrl"
        label="Recipe Url"
        variant="outlined"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <Button
        variant="outlined"
        onClick={handleParseWebsite}
        disabled={isLoading}
      >
        Parse Recipe
      </Button>

      {isLoading && (
        <div>
          <Grid
            container
            justifyContent="center"
            alignItems="center"
            style={{ marginTop: "20px" }}
          >
            <CircularProgress />
          </Grid>
        </div>
      )}
      {jsonRecipe && (
        <div>
          <Typography variant="h5" style={{ marginTop: "20px" }}>
            Parsed Data:
          </Typography>
          <Typography>
            {jsonRecipe.split("\n").map((i, key) => {
              return <div key={key}>{i}</div>;
            })}
          </Typography>
        </div>
      )}
      <TextField
        fullWidth
        id="txtJwt"
        label="Cookidoo jwt"
        variant="outlined"
        onChange={(e) => setJwt(e.target.value)}
      />
      <Button
        variant="outlined"
        onClick={handleParseWebsite}
        disabled={isLoading}
      >
        Import to Cookidoo
      </Button>
    </>
  );
}
