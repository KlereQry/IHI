format long

users = importdata('/lena16/dartagnan2/samper/data/selected.csv');

sillon = importdata('/lena16/dartagnan2/samper/data/Data_Sillons_IMAGEN/Imagen_mainSulcalMorphometry/mainmorpho_F.Coll._left.csv', ';');

sillSubj = str2num(cell2mat(sillon.textdata(2:end,1)));

index = [];

for i = 1:size(users.data(:,1),1)
    index(end+1) = find(sillSubj==users.data(i,1));
end

l = size(sillon.data,2);
m = zeros(l,2);

disp('Sillon collateral')
for k = 1:l
    [a,b] = corr(sillon.data(index,k), users.data(:,2));
    m(k,:) = [a,b];
end
m

sillon = importdata('/lena16/dartagnan2/samper/data/Data_Sillons_IMAGEN/Imagen_mainSulcalMorphometry/mainmorpho_S.Rh._left.csv', ';');

disp('Sillon rhinal')
l = size(sillon.data,2);
m = zeros(l,2);

for k = 1:l
    [a,b] = corr(sillon.data(index,k), users.data(:,2));
    m(k,:) = [a,b];
end
m


% T-test
IHI = users.data(:,2) >= 4;
nIHI = users.data(:,2) < 4;


sillon = importdata('/lena16/dartagnan2/samper/data/Data_Sillons_IMAGEN/Imagen_mainSulcalMorphometry/mainmorpho_F.Coll._left.csv', ';');

disp('Sillon collateral')
l = size(sillon.data,2);
m = zeros(l,4);

for k = 1:l
    
    d2 = sillon.data(index(IHI),k);
    d1 = sillon.data(index(nIHI),k);
    m(k,1) = mean(d1);
    m(k,2) = mean(d2);
    [h,p,ci,stats] = ttest2(d1,d2);
    m(k,3) = stats.tstat;
    m(k,4) = p;
end
m

sillon = importdata('/lena16/dartagnan2/samper/data/Data_Sillons_IMAGEN/Imagen_mainSulcalMorphometry/mainmorpho_S.Rh._left.csv', ';');

disp('Sillon rhinal')
l = size(sillon.data,2);
m = zeros(l,4);

for k = 1:l
    
    d1 = sillon.data(index(IHI),k);
    d2 = sillon.data(index(nIHI),k);
    m(k,1) = mean(d1);
    m(k,2) = mean(d2);
    [h,p,ci,stats] = ttest2(d1,d2);
    m(k,3) = stats.tstat;
    m(k,4) = p;
end
m


% ANOVA


% T-test
gIHI = users.data(:,3) == 1;
gPartialIHI = users.data(:,3) == -1;
gNoIHI = users.data(:,3) == 0;


sillon = importdata('/lena16/dartagnan2/samper/data/Data_Sillons_IMAGEN/Imagen_mainSulcalMorphometry/mainmorpho_F.Coll._left.csv', ';');

disp('ANOVA Sillon collateral')
l = size(sillon.data,2);
m = zeros(l,2);

for k = 1:l        
    [p,table] = anova1(sillon.data(index,k), users.data(:,3), 'off');
    m(k,2) = p;
    m(k,1) = cell2mat(table(2,5));
end
m
