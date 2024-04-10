document.addEventListener("DOMContentLoaded", () => {
    const allRecipeContainer = document.getElementById('all-recipe-container');
    const latestRecipeContainer = document.getElementById('latest-recipe-container');


    // Fetch all recipes
    fetch('/all_recipes')
        .then(response => response.json())
        .then(allRecipes => {
            // Populate all recipe cards
            allRecipes.forEach(recipe => {
                const card = createRecipeCard(recipe);
                allRecipeContainer.appendChild(card);
            });
        })
        .catch(error => console.error('Error fetching all recipes:', error));

    // Fetch latest recipes
    fetch('/latest_recipes')
        .then(response => response.json())
        .then(latestRecipes => {
            // Populate latest recipe cards
            latestRecipes.forEach(recipe => {
                const card = createRecipeCard(recipe);
                latestRecipeContainer.appendChild(card);
            });
        })
        .catch(error => console.error('Error fetching latest recipes:', error));

    // Function to create a recipe card
    function createRecipeCard(recipe) {
        const card = document.createElement('div');
        card.classList.add('card');
        card.innerHTML = `
            <img src="${recipe.image_path}" alt="${recipe.recipe_name}" class="w-full h-48 object-cover rounded-t-lg">
            <div class="m-4 flex-grow">
                <span class="font-bold">${recipe.recipe_name}</span>
                <span class="block text-gray-500 text-sm">Recipe by ${recipe.author}</span>
            </div>
            <div class="badge">
                <span>
                    <svg class="w-5 inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                    ${recipe.time} mins
                </span>
            </div>
        `;

        card.addEventListener('click', () => {
            // Redirect to recipe details page with recipe ID
            window.open(`/recipe-details/${recipe.id}`, '_blank');
        });
        return card;
    }
});
