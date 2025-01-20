library(ggplot2)
library(ggmap)

data <- read.delim('map.txt', row.names = 1, sep = '\t', stringsAsFactors = FALSE, check.names = FALSE,na.strings="na")
mp<-NULL 
mapworld<-borders("world",colour = NA,fill="#CCD8E0") 
mp<-ggplot()+mapworld+ylim(-90,90)+theme(panel.background = element_rect(color = NA , fill = 'transparent'), legend.key = element_rect(fill = 'transparent'))
mp2<-mp+geom_point(aes(x=data$lon,y=data$lat,size=6,color=data$`habitat`),alpha=0.6)+scale_size(range=c(1,8))+scale_color_manual(values=c("#66C2A5","#FC8D62","#E78AC3","#A6D854","#8DA0CB","#FFD92F"))
mp3 <- mp2 + 
  xlab("Longitude") + ylab("Latitude") + 
  theme(
    panel.border = element_rect(color = "black", fill = NA, size = 1), 
    axis.ticks = element_line(color = "black"),  
    axis.text.x = element_text(color = "black"),  
    axis.text.y = element_text(color = "black")   
  )
mp3 