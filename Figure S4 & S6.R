library(dplyr)
library(ggplot2)

df <- read.csv("shannon.csv")

summarized_data <- df %>%
  group_by(lat) %>%
  summarise(mean_shannon = mean(shannon, na.rm = TRUE)) %>%
  arrange(lat) 

x_min <- min(summarized_data$mean_shannon, na.rm = TRUE)
x_max <- max(summarized_data$mean_shannon, na.rm = TRUE)
x_range <- c(x_min - (x_max - x_min) * 0.1, x_max + (x_max - x_min) * 0.1) 

p <- ggplot(summarized_data, aes(x = mean_shannon, y = lat)) +
  geom_path(size = 1.2, color = "blue") + 
  geom_point(size = 3, color = "red") +  
  labs(x = "Mean Abundance", y = "Latitude (°)") + 
  theme_minimal() + 
  scale_y_continuous(breaks = seq(-90, 90, by = 30), limits = c(-90, 90)) + 
  scale_x_continuous(limits = c(6.3, 6.6), breaks = seq(6.2, 6.6, by = 0.1))+ 
  #scale_x_continuous(limits = x_range) + 
  theme(
    panel.border = element_rect(color = "black", fill = NA, size = 1), 
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),  
    axis.title = element_text(size = 12, face = "bold"), 
    axis.text = element_text(size = 10), 
    plot.margin = unit(c(1, 1, 1, 1), "cm") 
  ) 

print(p)