import express from "express";
import cors from "cors";
import * as RecipeAPI from './recipe-api';
import asyncHandler from "express-async-handler";
import dotenv from "dotenv";
dotenv.config();
const app = express();

app.use(express.json());
app.use(cors());


app.get(
  "/api/recipe/search",
  asyncHandler(async (req, res) => {
    const searchTerm = req.query.searchTerm as string;
    const page = parseInt((req.query.page as string) || "1", 10);
    const results = await RecipeAPI.searchRecipes(searchTerm, page);
    res.json(results);
  })
);

app.get("/api/recipes/:recipeId/summary", async ()=>{
  
})


app.listen(5000, () => {
  console.log("Server running on http://localhost:5000");
});
