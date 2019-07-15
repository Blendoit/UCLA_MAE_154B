function ds = get_ds(xi,xf,u)

dist = 0;
numSteps = 10;
dx = (xf-xi)/numSteps;
z0 = get_z(xi,u);
x0 = xi;
for i=1:10
    tempX = x0+dx;
    if tempX > 0
        tempZ = get_z(tempX,u);
    else 
        tempZ = 0;
    end
    dist = dist + (dx^2+(tempZ-z0)^2)^.5;
    z0 = tempZ;
    x0 = tempX;
end

ds =dist;