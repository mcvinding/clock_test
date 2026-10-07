###
# Example Intentional Binding (IB) Calculation Script in R
# This script are examples to inspect clock data (from import.R) and intentional binding effects 
# with plots. 
# for subjects with complete data.
# author: @mcvinding
###
library(ggplot2)
library(BayesFactor)

################################################################################
# Plotting the distribution of shiftTime for each condition
ggplot(clock.data, aes(x=shiftTime, fill=condition1)) +
  geom_density(alpha=0.5) +
  labs(title="Distribution of Shift Time by Condition",
       x="Shift Time (ms)",
       y="Density") +
  theme_minimal()

ggplot(clock.data, aes(x=shiftTime, fill=condition1)) +
  geom_density(alpha=0.5) +
  labs(title="Distribution of Shift Time by Condition per subj",
       x="Shift Time (ms)",
       y="Density") +
  theme_minimal()+
  facet_grid(~id)

################################################################################
# Plot intentional binding

# Plot the intentional binding effect for press
ggplot(ib.data, aes(x=condition, y=IB.press, fill=condition)) +
  stat_summary(fun=mean, geom="col") +
  stat_summary(fun.data=mean_se, geom="errorbar", width=0.2, color="black") +
  geom_jitter(aes(color=condition), width=0.12, alpha=0.6, size=1.8) +
  scale_color_manual(values=c("darkred", "darkblue")) +
  labs(title="Intentional Binding Effect (press)",
       x="Condition",
       y="Shift Time (ms)") +
  theme_minimal()

# Plot the intentional binding effect for tone
ggplot(ib.data, aes(x=condition, y=IB.tone, fill=condition)) +
  stat_summary(fun=mean, geom="col") +
  stat_summary(fun.data=mean_se, geom="errorbar", width=0.2, color="black") +
  geom_jitter(aes(color=condition), width=0.12, alpha=0.6, size=1.8) +
  scale_color_manual(values=c("darkred", "darkblue")) +
  labs(title="Intentional Binding Effect (tone)",
       x="Condition",
       y="Shift Time (ms)") +
  theme_minimal()


################################################################################
# Summary statistics
aggregate(IB.press ~ condition, data=ib.data, FUN=mean, na.rm=T)
aggregate(IB.tone ~ condition, data=ib.data, FUN=mean, na.rm=T)

ib.data.cl <- na.omit(ib.data)

press.self <- ib.data[ib.data$condition == "Self", c("id", "IB.press"),]
press.other <- ib.data[ib.data$condition == "Other", c("id", "IB.press"),]
press.paired <- merge(press.self, press.other, by="id", suffixes=c(".self", ".other"), sort=TRUE)

t.test(press.paired$IB.press.self, press.paired$IB.press.other, paired=TRUE)

tone.self <- ib.data[ib.data$condition == "Self", c("id", "IB.tone"),]
tone.other <- ib.data[ib.data$condition == "Other", c("id", "IB.tone"),]
tone.paired <- merge(tone.self, tone.other, by="id", suffixes=c(".self", ".other"), sort=TRUE)

t.test(tone.paired$IB.tone.self, tone.paired$IB.tone.other, paired=TRUE)

press.paired.cl <- na.omit(press.paired)
tone.paired.cl <- na.omit((tone.paired))

ttestBF(press.paired.cl$IB.press.self, press.paired.cl$IB.press.other, paired=TRUE)
ttestBF(tone.paired.cl$IB.tone.self, tone.paired.cl$IB.tone.other, paired=TRUE)
