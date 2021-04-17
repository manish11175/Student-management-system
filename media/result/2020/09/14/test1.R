x <- 3
typeof(x)

y<-2L
typeof(y)

z<-"SIRTS"
typeof(z)

c<-'s'
typeof(c)

f<-2.5
typeof(f)
print(x+y)
print(x*y)
print(x>y)
print(y>x)
print(x-y)
print(x/y)
print(x%%y)
print(10%/%5)





#for loop are used where iteration are defined
data<-LETTERS[1:26] 
for(i in data)
{
  print(i)
}

paste()
a<-"manish"
b<-"kunal"
paste(a,b)


#example

count<-1:40
for(i in  count )
{ print("manish")
  print(i)
}

# while loop are  used where when iteration are not define
#syntax
#While (logical expression)
#{ statement}


while(T)
  
{
  print('manish')
  
  break
}



count<-1
while(count<=12)
  {
 
  print("number")
  print(count)
  count<-count+1
  if(count==5)
  {
    break
  }
}

# nested loop
for(i in 1:10)
  {
  for(j in 1:10)
  {
    print(j)
  }
}


# if statement
#syntax- if (condition){statement }

for(i in 1:10){
  if(i<5)
    {
    print("manish")
  }
}

#random number generation

x<-rnorm(1)

if(x>1)
  {
  print(x)
  answer<-"greater than 1"
  print(answer)
}

else
{
  print(x)
  print("number is less than 1")
}
 
# function

# functon_name<-function(x=10) x*x
# function_name()
#function_name(argument)


intsum<-function(from=1,to=10)
{
  sum<-0
  for(i in from:to)
    sum<-sum+i
  sum
}
intsum(3)



#example


pow<-function(x,y){
  result<-x^y
  print(paste(x,"raised to the power",y,"is",result))
}
pow(2,4)

#vector it is basically an array it contains element of same datatype


my<-c(3,4,5,6,7,8)
v2<-c(3L,2L,4L,7L)
print(my)
print(v2)


v3<-c("a","hello",8)
is.character(v3)
print(v3)
# sequence function which generate sequence of number
v4<-seq(1,15)
print(v4)


v1<-c(1,2,3)
v2<-c(4,5,6)
v3<-v1*v2
print(v3)
print(v1/v2)
print(v1<v2)
print(v1>v2)


x<-rnorm(5)
x
for(i in x)
{
  print(i)
}
for(j in 1:5)
{
  print(x[j])
}



#matrix
B<-matrix(my_data,4,5,byrow=T)
print(B)

my_data<-1:20
A<-matrix(my_data,4,5)
print(A)


#matrix rbind() are used to bind row bind

r1<-c("i","am","manish")
r2<-c("what","a","day")
r3<-c(1,2,3)
C<-rbind(r1,r2,r3)
C

#column bind
c1<-1:5
c2<--1:5
D<-cbind(c1,c2)
D