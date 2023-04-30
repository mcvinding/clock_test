# Import data: clock part

folders <- c('~/clock_test/data')

subjects <- c(...)
conditions <- c("M-press1","M-press2","W-press1","W-press2")
in.files <- list.files()

# Import clock test data
setwd(folders[1])
sub.data <- data.frame()
clock.data <- data.frame()
for (sub in 1:length(subjects)){
  for (con in 1:length(conditions)){
    nam <- paste("data.sub",as.character(sub),".",conditions[con], sep="")
    
    temp.dat <- read.csv(paste(c("subject_",subjects[sub],"_",conditions[con],".csv"),collapse=''), sep=";",header=T)
    subID <- rep(as.character(sub),dim(temp.dat)[1])
    temp.dat <- temp.dat[,-(11:15)]
    
    recalc.1 <- ifelse(temp.dat$ansAngle < 100 & temp.dat$pressAngle > 270,T,F)
    temp.dat$ansAngle[recalc.1] <- temp.dat$ansAngle[recalc.1]+360               # +1,+H
    recalc.2 <- ifelse(temp.dat$ansAngle>260 & temp.dat$pressAngle<100,T,F)
    temp.dat$pressAngle[recalc.2] <- temp.dat$pressAngle[recalc.2]+360           # +H,+1    
    recalc <- recalc.1 | recalc.2
 
    errAngle <- temp.dat$ansAngle-temp.dat$pressAngle
    errTime <- errAngle*2550/360
    errTimeEMG <- errTime+65
  
#     extreme <- ifelse(errorTime > 500 | errorTime < -500,T,F)
    errors <- as.logical(temp.dat$userError) #| extreme
    errTime[errors] <- NA
    errTimeEMG[errors] <- NA

    report <- ifelse(conditions[con] == 'M-press'| conditions[con] == 'M-press1',"M","W")
    temp.dat <- cbind(temp.dat,errAngle,errTime,errTimeEMG,report,errors,recalc,subID)
    
    sub.data <- rbind(sub.data,temp.dat)
    assign(nam, temp.dat)
  }
  nim <- paste("data.sub",as.character(sub),".","all", sep="")
  assign(nim, sub.data)
  clock.data <- rbind(clock.data,sub.data)
}

# Save data
setwd(folders[3])
save("clock.data",file="clockData.RData")

# END