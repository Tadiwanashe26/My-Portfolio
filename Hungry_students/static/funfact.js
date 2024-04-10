const funFacts = [
    "Fun fact: Did you know that certain foods are known as 'brain foods' because they can help improve concentration and memory? Examples include blueberries, nuts, and dark chocolate. So, next time you're studying for an exam, consider snacking on these brain-boosting treats!",
    "Fun fact: Research suggests that students tend to indulge in late-night snacks more than other groups. Whether it's pizza after a study session or a bowl of cereal before bed, late-night snacking is a common habit among students.",
    "Fun fact: Instant ramen noodles are a staple in many college dorm rooms due to their affordability and convenience. In fact, it's estimated that college students consume billions of servings of instant ramen each year!",
    "Fun fact: Coffee is a beloved beverage among students, often relied upon to fuel late-night study sessions and early morning classes. Fun fact: The average college student drinks about three cups of coffee per day!",
    "Fun fact: For many students, managing a food budget is a key aspect of student life. Whether it's cooking budget-friendly meals at home or finding deals at the grocery store, students often become savvy budgeters when it comes to food expenses."
    ];


  // Function to display a random fun fact
  function displayRandomFunFact() {
    const randomIndex = Math.floor(Math.random() * funFacts.length);
    const randomFact = funFacts[randomIndex];
    const funFactElement = document.getElementById('fun-fact');
    funFactElement.textContent = randomFact;
  }
  window.onload = displayRandomFunFact;
