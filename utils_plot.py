from matplotlib import pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import os
import json


def plot_json(metadata, location, logger):
    with open(metadata, 'r') as file:
        data = json.load(file)

    # Convert JSON data into a DataFrame
    df = pd.DataFrame(data).T  # Transpose since JSON is nested by file name

    # Convert date strings to datetime objects
    df['date_UTC1'] = pd.to_datetime(df['date_UTC1'])

    # Sort by date
    df = df.sort_values(by='date_UTC1')

    # Plot temperature, battery voltage, and duration over time
    plt.figure(figsize=(12, 9))

    # Plot temperature
    plt.subplot(3, 1, 1)
    plt.plot(df['date_UTC1'], df['temperature'], marker='o', label='Temperature (°C)')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Over Time')
    plt.grid(True)
    plt.legend()

    # Plot battery voltage
    plt.subplot(3, 1, 2)
    plt.plot(df['date_UTC1'], df['battery_v'], marker='o', color='orange', label='Battery Voltage (V)')
    plt.xlabel('Date')
    plt.ylabel('Battery Voltage (V)')
    plt.title('Battery Voltage Over Time')
    plt.grid(True)
    plt.legend()

    # Plot duration
    plt.subplot(3, 1, 3)
    plt.plot(df['date_UTC1'], df['duration'], marker='o', color='green', label='Duration (seconds)')
    plt.xlabel('Date')
    plt.ylabel('Duration (seconds)')
    plt.title('Duration Over Time')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


def plot_temperature(df, metadata_folder_path, location, logger):
    """
    Plotting the results
    """
    # df index to datetime
    df.index = pd.to_datetime(df.index)

    # first date withouth time
    first_date = df.index[0].strftime("%Y-%m-%d")
    last_date = df.index[-1].strftime("%Y-%m-%d")

    # plot the results
    print(f"\n\nPlotting temperature in {location}")
    plt.figure(figsize=(20, 10))

    plt.scatter(df.index, df["temperature"], c=df["temperature"], cmap="inferno")
    plt.colorbar()
    
    plt.ylabel("Temperature (Celsius)")
    plt.xlabel("Time")
    plt.title(f"Temperature in {location} from {first_date} to {last_date}")

    # time interval
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=9))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

    # rotate and align the tick labels so they look better
    fig = plt.gcf()
    fig.autofmt_xdate()

    # make plot folder
    plot_folder = os.path.join(metadata_folder_path, "Plots")
    os.makedirs(plot_folder, exist_ok=True)

    # save the plot
    plt.savefig(f"{metadata_folder_path}/{location}_temperature.png")
    logger.info(f"Plot saved in {metadata_folder_path}/{location}_temperature.png")


def plot_battery(df, metadata_folder_path, location, logger):
    """
    Plotting the battery voltage over time with color changes for high and low levels.
    """
    df.index = pd.to_datetime(df.index)

    # first date withouth time
    first_date = df.index[0].strftime("%Y-%m-%d")
    last_date = df.index[-1].strftime("%Y-%m-%d")

    print(f"\nPlotting battery voltage in {location}")
    plt.figure(figsize=(20, 10))

    # Plot the battery voltage
    plt.plot(df.index, df['battery_v'])  # 'marker' to mark each data point

    plt.xlabel('Time')
    plt.ylabel('Battery Voltage (V)')
    plt.title(f'Battery Voltage over Time in {location}')

    # time interval
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=9))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

    # rotate and align the tick labels so they look better
    fig = plt.gcf()
    fig.autofmt_xdate()

    # make plot folder
    plot_folder = os.path.join(metadata_folder_path, "Plots")
    os.makedirs(plot_folder, exist_ok=True)

    # save the plot
    plt.savefig(f"{metadata_folder_path}/{location}_battery.png")


def plot_all_at_one(df, metadata_folder_path, location, logger):
    """
    Plotting the battery voltage over time with color changes for high and low levels.
    """
    df.index = pd.to_datetime(df.index)

    # first date withouth time
    first_date = df.index[0].strftime("%Y-%m-%d")
    last_date = df.index[-1].strftime("%Y-%m-%d")

    print(f"\nPlotting temperature and battery voltage in {location}")
    
    plt.figure(figsize=(20, 10))

    # set two y axis for temperature and battery
    ax1 = plt.gca()
    ax2 = ax1.twinx()

    # Plot the battery voltage
    ax2.plot(df.index, df['battery_v'], color='blue', label='Battery Voltage')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Battery Voltage (V)')
    ax2.tick_params(axis='y')

    # Plot the temperature
    ax1.plot(df.index, df['temperature'], color='red', label='Temperature')
    ax1.set_ylabel('Temperature (Celsius)')
    ax1.tick_params(axis='y')

    plt.title(f'Battery Voltage and Temperature in {location} from {first_date} to {last_date}')

    # time interval
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=9))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

    # rotate and align the tick labels so they look better
    fig = plt.gcf()
    fig.autofmt_xdate()

    # make plot folder
    plot_folder = os.path.join(metadata_folder_path, "Plots")
    os.makedirs(plot_folder, exist_ok=True)

    # save the plot
    plt.savefig(f"{plot_folder}/{location}_battery_temperature.png")


def plot_standar_deviation(df, metadata_folder_path, location, logger):
    """
    Plotting the battery voltage over time with color changes for high and low levels.
    """
    df.index = pd.to_datetime(df.index)

    # first date withouth time
    first_date = df.index[0].strftime("%Y-%m-%d")
    last_date = df.index[-1].strftime("%Y-%m-%d")

    print(f"\nPlotting temperature and battery voltage in {location}")
    
    plt.figure(figsize=(20, 10))

    # in two plots, plot the battery voltage and temperature standard deviation
    plt.subplot(2, 1, 1)
    plt.plot(df.index, df['battery_v'], color='blue', label='Battery Voltage')
    plt.xlabel('Time')
    plt.ylabel('Battery Voltage (V)')
    plt.title(f'Battery Voltage and Temperature in {location} from {first_date} to {last_date}')

    # time interval
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=9))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

    # rotate and align the tick labels so they look better
    fig = plt.gcf()
    fig.autofmt_xdate()

    plt.subplot(2, 1, 2)
    plt.plot(df.index, df['temperature'], color='red', label='Temperature')
    plt.xlabel('Time')
    plt.ylabel('Temperature (Celsius)')
    plt.tick_params(axis='y')

    # time interval
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=9))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

    # rotate and align the tick labels so they look better
    fig = plt.gcf()
    fig.autofmt_xdate()

    # make plot folder
    plot_folder = os.path.join(metadata_folder_path, "Plots")
    os.makedirs(plot_folder, exist_ok=True)

    # save the plot
    plt.savefig(f"{plot_folder}/{location}_battery_temperature.png")