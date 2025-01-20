library(ggplot2)
library(ggpubr)
library(readxl)

cor_data <- read_excel("rho.xlsx")
importance_data <- read_excel("importance.xlsx")

heatmap <- ggplot(cor_data, aes(x = gene, y = factor, fill = rho)) +
  geom_tile(color = "white", width = 0.9, height = 0.9) +  
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

heatmap <- heatmap +
  geom_text(data = subset(cor_data, pvalue > 0.05), aes(label = "x"), color = "black", size = 5)

bubble_chart <- heatmap +
  geom_point(data = importance_data, aes(size = importance), shape = 21, color = "black", fill = NA) +
  scale_size_continuous(range = c(1, 10))  

print(bubble_chart)