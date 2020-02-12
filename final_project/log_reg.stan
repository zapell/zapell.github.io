
data {
    // number obs
    int<lower=0> N;
    // num params
    int<lower=0> p;
    // variables
    int<lower=0, upper=1> outcome[N];
    vector[N] pregnancies;
    vector[N] glucose;
    vector[N] bloodPressure;
    vector[N] skinThickness;
    vector[N] insulin;
    vector[N] bmi;
    vector[N] dpf;
    vector[N] age;
}

parameters {
    real beta[p];
    real alpha;
}
/*
transformed parameters {
    // probability transformation
    //real<lower=0> odds[N];
    //real<lower=0, upper=1> prob[N];
    real prob[N];

    for (i in 1:N) {
        
        odds[i] <- exp(beta[1] + beta[2]*pregnancies[i] + beta[3]*glucose[i] + 
        beta[4]*bloodPressure[i] + beta[5]*skinThickness[i] + 
        beta[6]*insulin[i] + beta[7]*bmi[i] + beta[8]*dpf[i] 
        +beta[9]*age[i]);
        prob[i] <- odds[i]/(odds[i] + 1);
        
        prob[i] = beta[1] + beta[2]*pregnancies[i] + beta[3]*glucose[i] + 
        beta[4]*bloodPressure[i] + beta[5]*skinThickness[i] + 
        beta[6]*insulin[i] + beta[7]*bmi[i] + beta[8]*dpf[i] 
        +beta[9]*age[i];
    }
}
*/
model {
    beta ~ normal(0,5);
    alpha ~ normal(0,100);
    outcome ~ bernoulli_logit(alpha + beta[1]*pregnancies + 
    beta[2]*glucose + beta[3]*bloodPressure + beta[4]*skinThickness + 
    beta[5]*insulin + beta[6]*bmi + beta[7]*dpf + beta[8]*age);
}
