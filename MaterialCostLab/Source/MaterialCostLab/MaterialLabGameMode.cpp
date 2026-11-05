#include "MaterialLabGameMode.h"
#include "Camera/CameraActor.h"
#include "Camera/CameraComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMeshActor.h"
#include "GameFramework/PlayerController.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Modules/ModuleManager.h"

IMPLEMENT_PRIMARY_GAME_MODULE(FDefaultGameModuleImpl, MaterialCostLab, "MaterialCostLab");

namespace
{
UMaterialInterface* LoadLabMaterial(const FString& Name)
{
    return LoadObject<UMaterialInterface>(nullptr,*FString::Printf(TEXT("/Game/Lab/%s.%s"),*Name,*Name));
}

UStaticMeshComponent* Place(UWorld* World,UStaticMesh* Shape,UMaterialInterface* Material,
                            const FVector& Location,const FVector& Scale,const FRotator& Rotation)
{
    auto* Actor=World->SpawnActor<AStaticMeshActor>(Location,Rotation);
    auto* Mesh=Actor->GetStaticMeshComponent();
    Mesh->SetMobility(EComponentMobility::Movable);
    Mesh->SetStaticMesh(Shape);
    Mesh->SetWorldScale3D(Scale);
    Mesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    Mesh->SetCastShadow(false);
    Mesh->SetMaterial(0,Material);
    return Mesh;
}
}

AMaterialLabGameMode::AMaterialLabGameMode()
{
    DefaultPawnClass=nullptr;
}

void AMaterialLabGameMode::BeginPlay()
{
    Super::BeginPlay();
    FString Mode=TEXT("CPD");
    FParse::Value(FCommandLine::Get(),TEXT("MaterialMode="),Mode);
    const bool bCPD=Mode==TEXT("CPD"), bMID=Mode==TEXT("MID");
    const bool bGrid=bCPD || bMID;
    const FVector Eye(-700,0,0);
    auto* Camera=GetWorld()->SpawnActor<ACameraActor>(Eye,FRotator::ZeroRotator);
    Camera->GetCameraComponent()->SetProjectionMode(ECameraProjectionMode::Orthographic);
    Camera->GetCameraComponent()->SetOrthoWidth(1140);
    Camera->GetCameraComponent()->bConstrainAspectRatio=false;
    GetWorld()->GetFirstPlayerController()->SetViewTarget(Camera);
    auto* Material=LoadLabMaterial(TEXT("M_")+Mode);
    checkf(Material,TEXT("Unknown or missing material mode %s"),*Mode);
    if (bGrid)
    {
        auto* Cube=LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube"));
        check(Cube);
        for (int32 Row=0;Row<14;++Row)
        {
            for (int32 Column=0;Column<24;++Column)
            {
                const float Variation=float((Column+Row*3)%8)/7.0f;
                auto* Mesh=Place(GetWorld(),Cube,Material,FVector(0,(Column-11.5)*42,(Row-6.5)*42),
                                 FVector(0.32f),FRotator::ZeroRotator);
                if (bCPD) Mesh->SetCustomPrimitiveDataFloat(0,Variation);
                else
                {
                    auto* MID=UMaterialInstanceDynamic::Create(Material,Mesh);
                    MID->SetScalarParameterValue(TEXT("Variation"),Variation);
                    Mesh->SetMaterial(0,MID);
                }
            }
        }
    }
    else
    {
        auto* Plane=LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Plane.Plane"));
        check(Plane);
        Place(GetWorld(),Plane,Material,FVector::ZeroVector,FVector(10,5.6,1),FRotationMatrix::MakeFromZ(-FVector::ForwardVector).Rotator());
    }
    UE_LOG(LogTemp,Display,TEXT("MATERIAL_LAB_READY %s grid=%d"),*Mode,bGrid?336:0);
}
