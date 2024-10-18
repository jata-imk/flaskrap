export const fillMissingDates = function(ioHistory, startDate, endDate) {
    const filledHistory = [];
    let currentDate = new Date(startDate);
    const historyByDate = ioHistory.reduce((acc, item) => {
        acc[new Date(item.transaction_date).toISOString().split('T')[0]] = item;
        return acc;
    }, {});

    let lastPriceReaded = ioHistory[0]?.price;

    while (currentDate.getTime() <= new Date(endDate).getTime()) {
        const formatDate = new Date(currentDate).toISOString().split('T')[0];
        if (historyByDate[formatDate]) {
            filledHistory.push(historyByDate[formatDate]);

            lastPriceReaded = historyByDate[formatDate].price;
        } else {
            filledHistory.push({
                created_at: null,
                id: null,
                inventory_id: null,
                io_type: "PRICE_UPDATE",
                price: lastPriceReaded,
                quantity: 0,
                transaction_date: currentDate.toGMTString(),
                updated_at: null
            });
        }

        currentDate.setDate(currentDate.getDate() + 1);
    }

    return filledHistory;
}