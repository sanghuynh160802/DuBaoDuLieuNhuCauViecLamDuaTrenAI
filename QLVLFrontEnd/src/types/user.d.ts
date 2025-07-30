export interface IUser {
    id: string
    name: string
    password: string
    email: string
    updated_at: string
    created_at: string
    avatar: string
    user_type?: string
}
export interface ILogin {
    id?: string
    name?: string
    email: string
    password: string 
    avatar?: string,
    age?: number
    user_type?: string
}
export interface ISignUp {
    name: string
    email: string
    password: string 
    avatar: string,
    age: number
}
export interface IAuthState {
    user: ILogin
    isLoggedIn?: boolean
    isAdmin: boolean
}
export interface ISendMail {
    mailTo: string
    link: string
}
export interface IUpdate {
  id: string;
  name: string;
  email: string;
  age?: number;
  password?: string;
  avatar?: string;
  user_type?: string;
}
export interface IJobTitle {
    job: string
}
export interface IResetPass {
    email: string
    exp: number
    iat: number
}





