(function () {
    // Instance the tour
    var tour = new Tour({
        storage : false
    });
       tour.addSteps([
            {
                element: ".step1",
                title: "Are you a special one?",
                content: "If this is your first time visiting press next for a quick tour"
            },
            {
                element: ".step2",
                title: "Crystal Ball",
                content: "Accurate forecasting of predicted points based on the seasons data so far"
            },
            {
                element: ".step3",
                title: "Nerd Out",
                content: "Statistics on player attacking threat and team clean sheet potential"
            },
            {
                element: ".step4",
                title: "Surge",
                content: "Tailored and reliable transfer recommendations for your FPL team"
            }
        ]);

    // Initialize the tour
    tour.init();

    // Start the tour
    tour.start();
}());