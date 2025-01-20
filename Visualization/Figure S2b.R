library(ggplot2)
library(dplyr)
library(gridExtra)

data <- read.delim('test.txt', sep = '\t', stringsAsFactors = FALSE, check.names = FALSE)
all_abundance_data <- read.delim('all.txt', sep = '\t', stringsAsFactors = FALSE, check.names = FALSE)

colors <- c(
  "Reductive pentose phosphate cycle" = "blue", 
  "Methanogenesis, acetate => methane" = "green", 
  "CO oxidation" = "red",
  "3-Hydroxypropionate bi-cycle" = "yellow",
  "Dicarboxylate-hydroxybutyrate cycle" = "purple"
)

data_sorted <- data %>%
  mutate(Group = factor(Group, levels = names(colors))) %>%
  arrange(Group)

data_sorted <- data_sorted %>%
  mutate(Abundance_log = log10(Abundance + 1)) 

all_abundance_data <- all_abundance_data %>%
  mutate(Abundance_log = log10(Abundance + 1))

scatter_plot <- ggplot(data_sorted, aes(x = Abundance_log, y = reorder(Category, Coefficient), color = Group)) +
  geom_point(shape = 16, size = 3, alpha = 0.8) + 
  geom_point(data = all_abundance_data, aes(x = Abundance_log, y = Category), color = "grey", alpha = 0.5) +
  scale_color_manual(values = colors) +
  labs(
    x = "Log10(Abundance)", 
    y = NULL, 
    title = "Scatter Plot: Gene Abundance vs Coefficient"
  ) +
  theme_minimal() +
  theme(
    legend.position = "right",
    legend.title = element_blank(),
    panel.grid.minor = element_blank(),
    panel.grid.major.y = element_blank(),
    panel.background = element_rect(fill = "white", color = "black", size = 0.8), 
    plot.background = element_rect(fill = "white", color = NA), 
    plot.title = element_text(hjust = 0.5, size = 14, face = "bold"), 
    axis.text = element_text(size = 12),
    axis.title = element_text(size = 13, face = "bold")
  )

bar_plot <- ggplot(data_sorted, aes(x = reorder(Category, Coefficient), y = Coefficient, fill = Group)) +
  geom_col(width = 0.7) + 
  scale_fill_manual(values = colors) +
  labs(
    x = NULL, 
    y = "Coefficient", 
    title = "Bar Plot: Coefficients by Category"
  ) +
  coord_flip() + 
  theme_minimal() +
  theme(
    legend.position = "right",
    legend.title = element_blank(),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    panel.background = element_rect(fill = "white", color = "black", size = 0.8), 
    plot.background = element_rect(fill = "white", color = NA), 
    plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
    axis.text = element_text(size = 12),
    axis.title = element_text(size = 13, face = "bold")
  )

grid.arrange(scatter_plot, bar_plot, ncol = 2)
