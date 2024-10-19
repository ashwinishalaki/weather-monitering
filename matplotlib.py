import matplotlib.pyplot as plt

def visualize_weather_summary(city, summary):
    temps = [summary.avg_temp, summary.max_temp, summary.min_temp]
    labels = ['Avg Temp', 'Max Temp', 'Min Temp']
    
    plt.bar(labels, temps, color=['blue', 'red', 'green'])
    plt.title(f'{city} Weather Summary')
    plt.ylabel('Temperature (°C)')
    plt.show()
