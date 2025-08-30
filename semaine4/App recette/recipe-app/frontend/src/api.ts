export const searchRecipes = async (searchTerm: string, page: number) => {
  
  const baseURL = new URL("http://localhost:5000/api/recipe/search");
  baseURL.searchParams.append("searchTerm", searchTerm);
  baseURL.searchParams.append("page", page.toString());

  const response = await fetch(baseURL);

  if (!response.ok) {
    throw new Error(`HTTP Error: ${response.status}`);
  }

  return response.json();
};