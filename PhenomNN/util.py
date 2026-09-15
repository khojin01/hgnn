
import torch, math, numpy as np, scipy.sparse as sp
import torch.nn as nn, torch.nn.functional as F, torch.nn.init as init

def B2A(B,w=None,normalize_type="full"):
        #for alpha forward , we only have the diagonal value for adj and deg and laplacian,and they are thesame
        if w is None:
            if normalize_type=="edge":
                DE=diag((B ).sum(0)** (-1))
                L_alpha=None
                A_beta=B @ (DE) @ B.T
                I = torch.eye(A_beta.size(0), device=B.device)
                #
                A_beta=A_beta.to_dense()+I
                D_beta=diag(A_beta.to_sparse().sum(1))
            ####
            
            elif normalize_type=="full":

                DE=torch.diag(torch.pow((B ).sum(0),-1))
                L_alpha=None
                A_beta=B @ (DE) @ B.T
                I = torch.eye(A_beta.size(0), device=B.device)
                A_beta+=I
                #
                D_beta=torch.diag(A_beta.sum(1))
                D_beta_inv=D_beta**(-1/2)
                D_beta_inv[D_beta_inv == float("inf")] = 0
                A_beta=D_beta_inv@A_beta@D_beta_inv
                D_beta=torch.diag(A_beta.sum(1))
            elif normalize_type=="none":
                L_alpha=None
                A_beta=B  @ B.T
                I = torch.eye(A_beta.size(0), device=B.device)
                #
                A_beta=A_beta.to_dense()+I
                D_beta=diag(A_beta.to_sparse().sum(1))
            elif normalize_type=="node":
                L_alpha=None
                A_beta=B  @ B.T
                I = torch.eye(A_beta.size(0), device=B.device)
                A_beta+=I
                D_beta=torch.diag(A_beta.sum(1))
                D_beta_inv=D_beta**(-1/2)
                D_beta_inv[D_beta_inv == float("inf")] = 0
                A_beta=D_beta_inv@A_beta@D_beta_inv
                D_beta=torch.diag(A_beta.sum(1))
        else:
            if normalize_type=="edge":
                DE=diag((B ).sum(0)** (-1))
                DE=DE@w
                L_alpha=None
                A_beta=B @ (DE ) @ B.T
                I = torch.eye(A_beta.size(0), device=B.device)
                #
                A_beta=A_beta.to_dense()+I
                D_beta=diag(A_beta.to_sparse().sum(1))
            ####
            
            elif normalize_type=="full":
                
                DE=diag(torch.pow((B ).sum(0),-1))
                DE=DE@w
                L_alpha=None
                A_beta=B @ (DE) @ B.T
                I = torch.eye(A_beta.size(0), device=B.device)
                #
                A_beta=A_beta.to_dense()+I
                D_beta=diag(A_beta.to_sparse().sum(1))
            ####
                ##renormalization
                A_beta=D_beta**(-1/2) @ A_beta @ D_beta**(-1/2) 
                D_beta=diag(A_beta.to_sparse().sum(1))
            elif normalize_type=="none":

                L_alpha=None
                A_beta=B @ w @ B.T
                I = torch.eye(A_beta.size(0), device=B.device)
                #
                A_beta=A_beta.to_dense()+I
                D_beta=diag(A_beta.to_sparse().sum(1))
            elif normalize_type=="node":
                L_alpha=None
                A_beta=B @w @ B.T
                I = torch.eye(A_beta.size(0), device=B.device)
                #
                A_beta=A_beta.to_dense()+I
                D_beta=diag(A_beta.to_sparse().sum(1))
                A_beta=D_beta**(-1/2) @ A_beta @ D_beta**(-1/2) 
                D_beta=diag(A_beta.to_sparse().sum(1))
        return L_alpha,A_beta,D_beta,I