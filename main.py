import json
import requests
from tkinter import *
from tkinter import messagebox, Menu
import sqlite3

conn = sqlite3.connect('coin.db')
cobj = conn.cursor()


def Reset():
    for item in pycrp.winfo_children():
        item.destroy()
    AppHeader()
    my_portflio()

def my_portflio():

    cobj.execute("SELECT * FROM Coin_Details")
    conn.commit()
    coins = cobj.fetchall()
    a = len(coins)
    apikey = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=d4831bec-5bee-4706-836a-d96292e3465d")
    api = json.loads(apikey.content)

    def font_color(amt):
        if amt > 0:
            return 'green'
        else:
            return 'red'


    def insert_coin():
        cobj.execute("INSERT into Coin_Details(Symbol,Amount,Price) VALUES(?,?,?)",(symbol_txt.get(), amt_txt.get(), price_txt.get()))
        conn.commit()
        messagebox.showinfo("Portfolio Notification", "Coin Added Successfully")
        Reset()

    def update_coin():
        cobj.execute("Update Coin_Details SET Symbol = ?, Amount = ?,Price = ? WHERE ID =?",(symbol_txt1.get(), amt_txt1.get(), price_txt1.get(),portfolioID_txt.get()))
        conn.commit()
        messagebox.showinfo("Portfolio Notification", "Coin Updated Successfully")
        Reset()

    def delete_coin():
        cobj.execute("DELETE from Coin_Details where ID = ?",(portfolioID1_txt.get(),))
        conn.commit()
        messagebox.showinfo("Portfolio Notification","Coin Deleted Successfully")
        Reset()



    total_pl = 0
    coin_row = 1
    total_amt_paid = 0

    for i in range(0,300):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                amount_paid = coin[2] * coin[3]
                curr_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_per_coin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_per_coin * coin[2]
                total_pl += total_pl_coin
                total_amt_paid += amount_paid

                portfolio_ID = Label(pycrp, text=coin[0], bg="white", fg="#0C090A", font="lato 11 bold", borderwidth="2", relief="groove")
                portfolio_ID.grid(row=coin_row, column=0, sticky=N + E + S + W)

                name = Label(pycrp, text=api["data"][i]["symbol"], bg="white", fg="#0C090A",font ="lato 11 bold", borderwidth="2",relief = "groove")
                name.grid(row=coin_row, column=1, sticky=N + E + S + W)

                price = Label(pycrp, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="white", fg="#0C090A",font ="lato 11 bold", borderwidth="2",relief = "groove")
                price.grid(row=coin_row, column=2,sticky=N + E + S + W)

                c_owned = Label(pycrp, text=coin[2], bg="white", fg="#0C090A",font ="lato 11 bold", borderwidth="2",relief = "groove")
                c_owned.grid(row=coin_row, column=3, sticky=N + E + S + W)

                amt_paid = Label(pycrp, text="${0:.2f}".format(amount_paid), bg="white", fg="#0C090A",font ="lato 11 bold", borderwidth="2",relief = "groove")
                amt_paid.grid(row=coin_row, column=4, sticky=N + E + S + W)

                c_value = Label(pycrp, text="${0:.2f}".format(curr_value), bg="white", fg="#0C090A",font ="lato 11 bold", borderwidth="2",relief = "groove")
                c_value.grid(row=coin_row, column=5, sticky=N + E + S + W)

                profit_perCoin = Label(pycrp, text="${0:.2f}".format(pl_per_coin), bg="white", fg=font_color(pl_per_coin),font ="lato 11 bold", borderwidth="2",relief = "groove")
                profit_perCoin.grid(row=coin_row, column=6, sticky=N + E + S + W)

                tot_profit = Label(pycrp, text="${0:.2f}".format(total_pl_coin), bg="white", fg=font_color(total_pl_coin),font ="lato 11 bold", borderwidth="2",relief = "groove")
                tot_profit.grid(row=coin_row, column=7, sticky=N + E + S + W)

                tot_amount_paid = Label(pycrp, text="${0:.2f}".format(total_amt_paid), bg="white", fg=font_color(total_pl),font="lato 11 bold", borderwidth="2", relief="groove")
                tot_amount_paid.grid(row=coin_row + 1, column=4, sticky=N + E + S + W)

                tot_profit_amt = Label(pycrp, text="${0:.2f}".format(total_pl), bg="white",fg=font_color(total_pl), font="lato 11 bold", borderwidth="2",relief = "groove")
                tot_profit_amt.grid(row=coin_row+1, column=7, sticky=N + E + S + W)

                tot_profit_amt1 = Label(pycrp, text="Total Profit/Loss", bg="white", fg="black",font="lato 11 bold", borderwidth="2",relief = "groove")
                tot_profit_amt1.grid(row=coin_row + 1, column=0, sticky=N + E + S + W)

                print("Total Profit is {}".format(total_pl))

                apikey =""

                Refresh = Button(pycrp, text="Refresh", bg="#BCC6CC",fg="Black", command = Reset, font="lato 11 bold", borderwidth="2", relief = "groove")
                Refresh.grid(row=coin_row+2, column=7, sticky=N + E + S + W)
                coin_row += 1

    # Inserting Data
    symbol_txt = Entry(pycrp, borderwidth="2", relief="groove")
    symbol_txt.grid(row=coin_row + 1, column=2)

    price_txt = Entry(pycrp, borderwidth="2", relief="groove")
    price_txt.grid(row=coin_row + 1, column=3)

    amt_txt = Entry(pycrp, borderwidth="2", relief="groove")
    amt_txt.grid(row=coin_row + 1, column=4)

    Add_Coin = Button(pycrp, text="Add Coin", bg="#BCC6CC", fg="Black", command= insert_coin, font="lato 11 bold", borderwidth="2", relief="groove")
    Add_Coin.grid(row=coin_row + 1, column=5, sticky=N + E + S + W)

    #Updating Data
    portfolioID_txt = Entry(pycrp, borderwidth="2", relief="groove")
    portfolioID_txt.grid(row=coin_row + 2, column=1)

    symbol_txt1 = Entry(pycrp, borderwidth="2", relief="groove")
    symbol_txt1.grid(row=coin_row + 2, column=2)

    price_txt1 = Entry(pycrp, borderwidth="2", relief="groove")
    price_txt1.grid(row=coin_row + 2, column=3)

    amt_txt1 = Entry(pycrp, borderwidth="2", relief="groove")
    amt_txt1.grid(row=coin_row + 2, column=4)

    Update_Coin = Button(pycrp, text="Update Coin", bg="#BCC6CC", fg="Black", command=update_coin, font="lato 11 bold", borderwidth="2", relief="groove")
    Update_Coin.grid(row=coin_row + 2, column=5, sticky=N + E + S + W)

    portfolioID1_txt = Entry(pycrp, borderwidth="2", relief="groove")
    portfolioID1_txt.grid(row=coin_row + 3, column=4)

    Delete_Coin = Button(pycrp, text="Delete Coin", bg="#BCC6CC", fg="Black", command=delete_coin, font="lato 11 bold", borderwidth="2", relief="groove")
    Delete_Coin.grid(row=coin_row + 3, column=5, sticky=N + E + S + W)


def AppHeader():
    portfolio_Id = Label(pycrp, text="Portfolio ID", bg="#7FFFD4", fg="#2B1B17", font="lato 12 bold", borderwidth="2")
    portfolio_Id.grid(row=0, column=0, sticky=N + E + S + W)

    name = Label(pycrp, text = "Coin Name", bg ="#7FFFD4", fg = "#2B1B17" ,font ="lato 12 bold", borderwidth="2")
    name.grid(row=0,column=1, sticky = N+E+S+W)

    price = Label(pycrp, text = "Price", bg = "#7FFFD4", fg = "#2B1B17",font ="lato 12 bold", borderwidth="2")
    price.grid(row=0,column=2,sticky=N + E + S + W)

    c_owned = Label(pycrp, text = "Coins Owned", bg = "#7FFFD4", fg = "#2B1B17",font ="lato 12 bold", borderwidth="2")
    c_owned.grid(row=0,column=3, sticky=N + E + S + W)

    amt_paid = Label(pycrp, text = "Total Amount Paid", bg = "#7FFFD4", fg = "#2B1B17",font ="lato 12 bold", borderwidth="2")
    amt_paid.grid(row=0,column=4, sticky=N + E + S + W)

    c_value = Label(pycrp, text = "Current Value", bg = "#7FFFD4", fg = "#2B1B17",font ="lato 12 bold" ,borderwidth="2")
    c_value.grid(row=0,column=5, sticky=N + E + S + W)

    profit_perCoin = Label(pycrp, text = "P/L Per Coin", bg = "#7FFFD4", fg = "#2B1B17",font ="lato 12 bold" ,borderwidth="2")
    profit_perCoin.grid(row=0,column=6, sticky=N + E + S + W)

    tot_profit = Label(pycrp, text = "Total P/L per Coin", bg = "#7FFFD4", fg = "#2B1B17",font ="lato 12 bold" ,borderwidth="2")
    tot_profit.grid(row=0,column=7, sticky=N + E + S + W)


pycrp = Tk()
pycrp.title("My Crypto Portfolio")
AppHeader()
my_portflio()
pycrp.mainloop()

cobj.close()
conn.close()


