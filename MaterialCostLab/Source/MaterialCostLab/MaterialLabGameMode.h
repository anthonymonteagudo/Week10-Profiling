#pragma once
#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "MaterialLabGameMode.generated.h"

UCLASS()
class AMaterialLabGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    AMaterialLabGameMode();
    virtual void BeginPlay() override;
};
